from fastapi import APIRouter, UploadFile
from src.field_representation.pipeline import field_processing



router = APIRouter(prefix="/predict")


@router.post("/one_image")
async def one_image_prediction(file: UploadFile):

    data = await file.read()
    image, bboxes, geo_coords = field_processing(data)

    return {"msg": "ok"}