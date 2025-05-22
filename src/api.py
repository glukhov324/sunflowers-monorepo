from fastapi import APIRouter, UploadFile
import numpy as np
import cv2
from src.segmentation import get_yolo_prediction



router = APIRouter(prefix="/predict")


@router.post("/one_image")
async def one_image_prediction(file: UploadFile):

    data = await file.read()
    nparr = np.fromstring(data, np.uint8)
    bgr_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    prediciton = get_yolo_prediction(bgr_image=bgr_img)

    return {"msg": "ok"}