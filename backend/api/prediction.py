from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends

from sqlalchemy.orm import Session

from backend.api.dependencies import get_current_user

from backend.db.database import get_db

from backend.models.prediction import Prediction

from backend.services.prediction_service import predict_digit

from backend.core.s3 import upload_image

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


@router.post("/")
async def predict(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    file_bytes = await file.read()

    result = predict_digit(
        file_bytes
    )

    image_url = upload_image(
        file_bytes,
        file.filename
    )

    processed_url = upload_image(
        result["processed_bytes"],
        f"processed-{file.filename}"
    )

    prediction_row = Prediction(
        image_url=image_url,
        processed_image_url=processed_url,
        predicted_digit=result["digit"],
        confidence=result["confidence"],
        user_id=current_user.id
    )

    db.add(prediction_row)

    db.commit()

    db.refresh(prediction_row)

    return {
        "prediction_id": prediction_row.id,
        "prediction": result["digit"],
        "confidence": result["confidence"],
        "image_url": image_url,
        "processed_image_url": processed_url
    }