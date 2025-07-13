import numpy as np
from src.schemas import BoundingBox
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
  

  def apply_mask(self, masks):
    """
    Составление маски для фрагмента поля
    """

    if masks is not None:
      for mask in masks:
        mask = mask.numpy().astype(np.uint8)
        self.mask += mask
                     
      self.mask[self.mask != 0] = 1