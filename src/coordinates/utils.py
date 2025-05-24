import numpy as np
from src.settings import settings


def pixel2degree(camera_lat: float,
                 camera_lon: float,
                 x_obj: float, 
                 y_obj: float) -> tuple[float, float]:
    """
    Перевод пикселей в градусы широты и долготы
    """

    # перевод пикселей в метры
    offset_x_m = x_obj * settings.METERS_PER_PIXEL
    offset_y_m = - y_obj * settings.METERS_PER_PIXEL

    # перевод метров в градусы
    delta_lat = offset_y_m / settings.R_EARTH * (180 / np.pi)
    delta_lon = offset_x_m / (settings.R_EARTH * np.cos(np.pi * camera_lat / 180)) * (180 / np.pi)

    return (camera_lat + delta_lat, camera_lon + delta_lon)