import numpy as np
from typing import List
from src.field_representation.bounding_box import BoundingBox
from src.field_representation.crop import Crop



class Field:
    """
    Класс для представления поля.

    Attributes:
        image (np.ndarray) : изображение в виде массива numpy
        mask (np.ndarray) : карта растительности (маска) для поля
        win_size (tuple[int, int]) : размер окна для разрезания поля на фрагменты
        stride (tuple[int, int]) : шаг разреза поля на фрагменты
        crops (List[Crop]) : список фрагментов изображения
        bboxes (List[BoundingBox]) : список bounding box-ов объектов на всём поле
    
    Methods:
        crop_image(): деление изображения на фрагменты
        get_mask_boxes(): получение карты растительности (маски) и bounding box'ов для всего поля
        count_plants(): подсчет количества единиц культурных растений на поле
    """

    def __init__(self, 
                image: np.ndarray, 
                win_size: tuple[int, int],
                stride: tuple[int, int]):

        self.image = image
        self.mask = np.zeros((image.shape[0], image.shape[1]))
        self.win_size = win_size
        self.stride = stride
        self.crops: List[Crop] = []
        self.bboxes: List[BoundingBox] = []

  

    def crop_image(self):
        """
        Деление изображения на фрагменты
        """

        if self.image is None:
            return
    
        dx, dy = self.win_size
        sx, sy = self.stride
        for x in range(0, self.image.shape[0], sx):
            for y in range(0, self.image.shape[1], sy):
                diff_x = x + dx - self.image.shape[0]
                diff_y = y + dy - self.image.shape[1]
                # по краям отступаем назад и считываем оставшиеся
                # фрагменты изображения в ряде
                if diff_x > 0:
                    x -= diff_x
                if diff_y > 0:
                    y -= diff_y

                self.crops.append(
                    Crop(image=self.image[x : x + dx, y : y + dy],
                         borders=BoundingBox(x, y, x+dx, y+dy))        
                )

    def get_mask_boxes(self):
        """
        Получение карты растительности (маски) и bounding box'ов для всего поля 
        """

        for i in range(len(self.crops)):
            self.crops[i].get_plants_bboxes_masks()
            crop_mask = self.crops[i].mask.astype(np.uint8)
            mask_borders = self.crops[i].borders
            self.mask[mask_borders.xu:mask_borders.xd, mask_borders.yu: mask_borders.yd] += crop_mask
            self.bboxes.extend(self.crops[i].bboxes_scaled)

        self.mask[self.mask != 0] = 1
    
        
    def count_plants(self):
        """
        Подсчет количества единиц культурных растений на поле
        """

        return len(self.bboxes)