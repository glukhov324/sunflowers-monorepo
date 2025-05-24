import supervision as sv
import numpy as np
from src.settings import settings
from src.segmentation.model import model



def get_yolo_prediction(bgr_image: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    
    yolo_predictions_source = model(source=bgr_image)[0]
    yolo_predictions_nms = sv.Detections.from_ultralytics(
        yolo_predictions_source
    ).with_nms(threshold=settings.NMS_THRESHOLD_MODEL, class_agnostic=True)

    return (yolo_predictions_nms.xyxy, yolo_predictions_nms.mask, yolo_predictions_nms.confidence)