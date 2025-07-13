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
    lat: float | None
    lon: float | None

class SunflowerItem(BaseModel):
    bbox: BoundingBox
    geo_coords: GeoCoords

class MLServiceResponse(BaseModel):
    img_base64: str
    sunflowers_data: List[SunflowerItem]