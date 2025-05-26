import PIL
import PIL.Image
import numpy as np
from typing import List
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
        self.bboxes: List[BoundingBox] = []
        self.confs: List[float] = []
        self.boxes_geo_coords: List[GeoCoords] = []

  

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

        for i in range(len(self.crops)):
            self.crops[i].get_plants_bboxes_masks()
            crop_mask = self.crops[i].mask.astype(np.uint8)
            mask_borders = self.crops[i].borders
            self.mask[int(mask_borders.xu):int(mask_borders.xd), int(mask_borders.yu):int(mask_borders.yd)] += crop_mask
            self.bboxes.extend(self.crops[i].bboxes_scaled)
            self.confs.extend(self.crops[i].confs)

        self.mask[self.mask != 0] = 1
        self.confs = [item for sublist in self.confs for item in sublist]
        self.bboxes, self.confs = cv2_nms(boxes=self.bboxes,
                                          confs=self.confs,
                                          confs_threshold=settings.CONFS_THRESHOLD,
                                          nms_threshold=settings.NMS_THRESHOLD_BOXES)

    def geo_boxes_coords(self):
        """
        Получение географических координат центров bounding box'ов объектов
        """

        camera_lat, camera_lon = get_camera_coords(pil_img=self.pil_image)
        image_width_px = self.image_array.shape[1]
        image_height_px = self.image_array.shape[0]

        for box in self.bboxes:
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

        return len(self.bboxes)