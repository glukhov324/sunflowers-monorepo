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
                xu = 0, 
                yu = 0, 
                xd = 0, 
                yd = 0):
        
        self.xu = xu
        self.yu = yu
        self.xd = xd
        self.yd = yd