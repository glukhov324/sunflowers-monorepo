import PIL
from PIL.ExifTags import TAGS, GPSTAGS
from typing import List



def parse_gps_coordinate(tags):
    """
    Преобразование координат вида (градусы, минуты, секунды) в десятичные градусы
    """

    degrees, minutes, seconds = tags
    return float(degrees) + float(minutes) / 60 + float(seconds) / 3600


def get_camera_coords(pil_img: PIL.Image) -> List:
    """
    Получение широты и долготы из метаданных изображения
    """
    
    exif = pil_img._getexif()
    # Ищем GPS-информацию
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == "GPSInfo":
            gps_data = {}
            for t in value:
                sub_tag = GPSTAGS.get(t, t)
                gps_data[sub_tag] = value[t]
            
            # Парсим координаты
            lat = parse_gps_coordinate(gps_data['GPSLatitude'])
            lat_ref = gps_data.get('GPSLatitudeRef', 'N')
            lon = parse_gps_coordinate(gps_data['GPSLongitude'])
            lon_ref = gps_data.get('GPSLongitudeRef', 'E')

            # Учитываем направление
            if lat_ref != 'N':
                lat = -lat
            if lon_ref != 'E':
                lon = -lon
            return [lon, lat]
        else:
            return []