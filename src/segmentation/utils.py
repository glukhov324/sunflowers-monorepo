# import numpy as np



# class Field:
#   """
#   Класс для представления поля.

#   image - изображение в виде массива numpy
#   mode - режим работы с объектом
#   mask - карта растительности (маска) для поля
#   win_size - размер окна для разрезания поля на фрагменты
#   stride - шаг разреза поля на фрагменты
#   number_of_plants - количество единиц культурных растений
#                      на поле
#   samples - список фрагментов изображения
#   bboxes_list - список bounding box-ов
#   """
  
#   def __init__(self, 
#                image: np.ndarray | None = None, 
#                win_size: tuple = (256, 256),
#                stride: tuple = (64, 64)
#               ):
    
#     self.image = image
#     self.mask = np.zeros(self.image.shape)
#     self.win_size = win_size
#     self.stride = stride
#     self.number_of_plants = 0
#     self.samples = []
#     self.bboxes = []

#   def samples2union(self):
#     """
#     Объединяет маски фрагментов изображения в
#     единую маску поля.
#     """
#     for sample in self.samples:
#       xu, yu, xd, yd = sample.borders
#       self.mask[xu: xd, yu: yd] = sample.image 

#   def crop2sample(self):
#     """
#     Разрезает изображение на фрагменты.
#     """
#     if self.image is None:
#       return
#     dx, dy = self.win_size
#     sx, sy = self.stride
#     for x in range(0, self.image.shape[0], sx):
#       for y in range(0, self.image.shape[1], sy):
#         diff_x = x + dx - self.image.shape[0]
#         diff_y = y + dy - self.image.shape[1]
#         # по краям отступаем назад и считываем оставшиеся
#         # фрагменты изображения в ряде
#         if diff_x > 0:
#           x -= diff_x
#         if diff_y > 0:
#           y -= diff_y

#         self.samples.append(
#             Sample(self.image[x : x + dx, y : y + dy],
#             Rectangle(x, y, x+dx, y+dy),
#             self.mask[x : x + dx, y : y + dy])
#             )
        
#   def count_plants(self):
#     """
#     Подсчитывает количество единиц культурных растений на поле.
#     """
#     self.number_of_plants = len(self.bboxes)
#     return self.number_of_plants