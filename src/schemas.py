from pydantic import BaseModel
from typing import List



class BoundingBox(BaseModel):
    xu: float
    yu: float
    xd: float
    yd: float

    def tolist(self):
        return [self.xu, self.yu, self.xd, self.yd]

class GeoCoords(BaseModel):
    lat: float
    lon: float

class MLServiceResponse(BaseModel):
    img_base64: str
    bboxes: List[BoundingBox]
    geo_coords: List[GeoCoords]