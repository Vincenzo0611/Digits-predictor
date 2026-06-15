import os
import uuid

from backend.core.config import UPLOAD_DIR
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends

from backend.services.prediction_service import predict_digit

from backend.api.dependencies import get_current_user

from sqlalchemy.orm import Session

from backend.db.database import get_db

from backend.models.prediction import Prediction

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def predict(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    filename = f"{uuid.uuid4()}.png"

    file_path = os.path.join(   
        UPLOAD_DIR,
        filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = predict_digit(file_path)

    prediction_row = Prediction(
        image_path=filename,
        processed_image_path=result["processed_image"],
        predicted_digit=result["digit"],
        confidence=result["confidence"],
        user_id=current_user.id
    )

    db.add(prediction_row)

    db.commit()

    db.refresh(prediction_row)

    return {
        "filename": filename,
        "prediction": result["digit"],
        "confidence": result["confidence"],
        "processed_image": result["processed_image"]
    }