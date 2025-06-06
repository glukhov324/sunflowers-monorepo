import cv2
import numpy as np
from typing import List, Dict
from src.schemas import BoundingBox



def cv2_nms(boxes: List[BoundingBox], 
            confs: Dict[int, List[float]], 
            confs_threshold: float = 0.7, 
            nms_threshold: float = 0.5) -> tuple[List[BoundingBox], List[float]]:
    
        boxes_list = [box.tolist() for box in boxes]
        confs = [float(conf) for key in confs for conf in confs[key]]
        indices = cv2.dnn.NMSBoxes(bboxes=boxes_list, 
                                   scores=confs, 
                                   score_threshold=confs_threshold, 
                                   nms_threshold=nms_threshold)
        
        filtered_boxes = [boxes[i] for i in indices.flatten()]
        filtered_confs = [confs[i] for i in indices.flatten()]

        print(len(filtered_boxes))

        return filtered_boxes, filtered_confs