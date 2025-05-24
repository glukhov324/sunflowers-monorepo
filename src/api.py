from fastapi import APIRouter, UploadFile
from src.field_representation.pipeline import field_processing
from src.schemas import MLServiceResponse



router = APIRouter(prefix="/predict")


@router.post("/one_image")
async def one_image_prediction(file: UploadFile) -> MLServiceResponse:

    image_data = await file.read()
    response = field_processing(image_data)

    return response