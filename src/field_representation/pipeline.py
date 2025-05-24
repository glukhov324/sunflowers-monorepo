from PIL import Image
import numpy as np
import cv2
import io
from loguru import logger
from src.field_representation import Field
from src.settings import settings



def field_processing(image_data: str):
    pil_image = Image.open(io.BytesIO(image_data))
    nparr = np.fromstring(image_data, np.uint8)
    bgr_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    field = Field(
        pil_image=pil_image,
        image=bgr_img,
        win_size=(settings.WIN_SIZE, settings.WIN_SIZE),
        stride=(settings.STRIDE, settings.STRIDE),
    )

    logger.info("Crop image process was started")
    field.crop_image()
    logger.info("Crop image process was ended")

    logger.info("Predict masks and bboxes for each crop process was started")
    field.get_mask_boxes()
    logger.info("Predict masks and bboxes for each crop process was ended")

    logger.info("Get geo coordinates of sunflowers process was started")
    field.geo_boxes_coords()
    logger.info("Get geo coordinates of sunflowers process was ended")

    return field.image, field.bboxes, field.boxes_geo_coords