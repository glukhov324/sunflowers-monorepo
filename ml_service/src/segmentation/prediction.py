import numpy as np
from src.segmentation.model import model
from typing import List
import ultralytics



def get_yolo_prediction(bgr_images: List[np.ndarray]) -> ultralytics.engine.results.Results:
    
    yolo_predictions_source = model(source=bgr_images)

    return yolo_predictions_source