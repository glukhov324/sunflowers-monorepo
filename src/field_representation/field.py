import PIL
import PIL.Image
import numpy as np
from typing import List, Dict
from src.segmentation.prediction import get_yolo_prediction
from src.field_representation import Crop
from src.schemas import BoundingBox, GeoCoords
from src.segmentation import cv2_nms
from src.coordinates import get_camera_coords, pixel2degree
from src.settings import settings



class Field:
    """
    Класс для представления поля

    Attributes:
        pil_image (PIL.Image): изображение поля в формате PIL.Image
        image (np.ndarray): изображение поля в виде массива numpy
        mask (np.ndarray): карта растительности (маска) для поля
        win_size (tuple[int, int]): размер окна для разрезания поля на фрагменты
        stride (tuple[int, int]): шаг разреза поля на фрагменты
        crops (List[Crop]): список фрагментов изображения
        bboxes (List[BoundingBox]): список bounding box-ов объектов на всём поле
    """

    def __init__(self,
                 pil_image: PIL.Image,
                 image_array: np.ndarray, 
                 win_size: tuple[int, int],
                 stride: tuple[int, int]):

        self.pil_image: PIL.Image = pil_image
        self.image_array: np.ndarray = image_array
        self.mask: np.ndarray = np.zeros((image_array.shape[0], image_array.shape[1]))
        self.win_size: tuple[int, int] = win_size
        self.stride: tuple[int, int] = stride
        self.crops: List[Crop] = []
        self.confs: List[float] = []
        self.boxes_geo_coords: List[GeoCoords] = []
        self.scaled_bboxes = []

  

    def crop_image(self):
        """
        Деление изображения на фрагменты
        """

        if self.image_array is None:
            return
    
        dx, dy = self.win_size
        sx, sy = self.stride
        for x in range(0, self.image_array.shape[0], sx):
            for y in range(0, self.image_array.shape[1], sy):
                diff_x = x + dx - self.image_array.shape[0]
                diff_y = y + dy - self.image_array.shape[1]

                if diff_x > 0:
                    x -= diff_x
                if diff_y > 0:
                    y -= diff_y

                self.crops.append(
                    Crop(image=self.image_array[x : x + dx, y : y + dy],
                         borders=BoundingBox(xu=x, yu=y, xd=x+dx, yd=y+dy))        
                )
                

    def get_mask_boxes(self):
        """
        Получение карты растительности (маски) и bounding box'ов для всего поля 
        """
        start = 0
        confs, crops_bboxes, crops_masks = {}, {}, {}
        for i in range(0, len(self.crops), settings.BATCH_SIZE):
            crops_list = [elem.image for elem in self.crops[start:start + settings.BATCH_SIZE]]
            pred_result = get_yolo_prediction(bgr_images=crops_list)
            start += settings.BATCH_SIZE

            
            for i, r in enumerate(pred_result):
                boxes = r.boxes
                if r.masks:
                    crops_bboxes[len(crops_bboxes)] = boxes.xyxy.cpu()
                    confs[len(confs)] = boxes.conf.cpu()
                    crops_masks[len(crops_masks)] = r.masks.data.cpu()
                else:
                    crops_bboxes[len(crops_bboxes)] = []
                    confs[len(confs)] = []
                    crops_masks[len(crops_masks)] = []

                    
        for i in range(len(self.crops)):
            current_crop_masks = crops_masks[i]
            self.crops[i].apply_mask(masks=current_crop_masks)

            crop_mask = self.crops[i].mask.astype(np.uint8)
            mask_borders = self.crops[i].borders
            self.mask[int(mask_borders.xu):int(mask_borders.xd), int(mask_borders.yu):int(mask_borders.yd)] += crop_mask

            self.scaled_bboxes.extend([
                    BoundingBox(xu=box[0] + self.crops[i].borders.yu,
                                yu=box[1] + self.crops[i].borders.xu,
                                xd=box[2] + self.crops[i].borders.yu,
                                yd=box[3] + self.crops[i].borders.xu)  for box in crops_bboxes[i] if box != []
                ])
                                                                            
        self.scaled_bboxes, self.confs = cv2_nms(boxes=self.scaled_bboxes,
                                                confs=confs,
                                                confs_threshold=settings.CONFS_THRESHOLD,
                                                nms_threshold=settings.NMS_THRESHOLD_BOXES)
        del confs, crops_bboxes, crops_masks

    def geo_boxes_coords(self):
        """
        Получение географических координат центров bounding box'ов объектов
        """

        camera_lat, camera_lon = get_camera_coords(pil_img=self.pil_image)
        image_width_px = self.image_array.shape[1]
        image_height_px = self.image_array.shape[0]

        for box in self.scaled_bboxes:
            x_center_object = (box.xd - box.xu) / 2
            y_center_object = (box.yd - box.yu) / 2

            offset_x_px = x_center_object - image_width_px / 2
            offset_y_px = y_center_object - image_height_px / 2

            geo_coords = pixel2degree(camera_lat=camera_lat, 
                                      camera_lon=camera_lon, 
                                      x_obj=offset_x_px, 
                                      y_obj=offset_y_px)
            
            self.boxes_geo_coords.append(geo_coords)


    def count_plants(self) -> int:
        """
        Подсчет количества единиц культурных растений на поле
        """

        return len(self.scaled_bboxes)