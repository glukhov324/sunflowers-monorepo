from ultralytics import YOLO
from src.settings import settings



def get_yolo(path: str) -> YOLO:
    return YOLO(path)


model = get_yolo(settings.MODEL_PATH)