import numpy as np
from typing import List
from src.schemas import BoundingBox
from src.segmentation import get_yolo_prediction
from src.settings import settings



class Crop:
  """
  Класс для представления фрагмента изображения

  Attributes:
    image (np.ndarray): изображение в виде массива numpy
    borders (BoundingBox) - границы изображения в исходном фото
    mask (np.ndarray): - карта растительности (маска) для фрагмента изображения

  """
  def __init__(self,
               image: np.ndarray,
               borders: BoundingBox):
    
    self.image = image
    self.borders = borders
    self.mask = np.zeros((settings.WIN_SIZE, settings.WIN_SIZE))
    self.bboxes_crop: List[BoundingBox] = []
    self.bboxes_scaled: List[BoundingBox] = []
    self.confs = []
  

  def get_plants_bboxes_masks(self):
    """
    Получение маски и bounding box-ов для фрагмента поля
    """
    bboxes, masks, conf = get_yolo_prediction(bgr_image=self.image)
    if masks is not None:
      for i, mask in enumerate(masks):
        self.mask += mask.astype(np.uint8)
        cur_box = bboxes[i]
        self.bboxes_crop.append(BoundingBox(xu=cur_box[0],
                                            yu=cur_box[1],
                                            xd=cur_box[2],
                                            yd=cur_box[3]))
        
        self.bboxes_scaled.append(BoundingBox(xu=cur_box[0] + self.borders.yu,
                                              yu=cur_box[1] + self.borders.xu,
                                              xd=cur_box[2] + self.borders.yu,
                                              yd=cur_box[3] + self.borders.xu))
      self.confs.append(conf.tolist())
                          
      self.mask[self.mask != 0] = 1