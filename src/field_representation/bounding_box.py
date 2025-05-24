


class BoundingBox:
    """
    Класс для представления bounding box'a.

    Attributes:
        xu (float): координата по x левого верхнего угла
        yu (float): координата по y левого верхнего угла
        xd (float): координата по x левого нижнего угла
        yd (float): координата по y левого нижнего угла
    """
    
    def __init__(self, 
                 xu: float = 0.0, 
                 yu: float = 0.0, 
                 xd: float = 0.0, 
                 yd: float = 0.0):
        
        self.xu = xu
        self.yu = yu
        self.xd = xd
        self.yd = yd
    
    def tolist(self):
        """
        Преобразует объект класса bounding box в список [xu, yu, xd, yd]
        """

        return [self.xu, self.yu, self.xd, self.yd]