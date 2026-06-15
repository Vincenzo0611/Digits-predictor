import os

from backend.core.config import PROCESSED_DIR, UPLOAD_DIR
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from pydantic import BaseModel

from sqlalchemy.orm import Session

from backend.db.database import get_db

from backend.models.prediction import Prediction

from backend.api.dependencies import get_current_user

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)


class FeedbackRequest(BaseModel):
    prediction_id: int
    is_correct: bool
    correct_digit: int | None = None


@router.post("/")
def give_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    prediction = (
        db.query(Prediction)
        .filter(
            Prediction.id == request.prediction_id
        )
        .first()
    )

    if not prediction:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    prediction.is_correct = request.is_correct

    if request.is_correct:

        image_path = os.path.join(
            UPLOAD_DIR,
            prediction.image_path
        )

        processed_path = os.path.join(
            PROCESSED_DIR,
            prediction.processed_image_path
        )

        if os.path.exists(image_path):
            os.remove(image_path)

        if os.path.exists(processed_path):
            os.remove(processed_path)
        
        db.delete(prediction)

    else:
        prediction.correct_digit = (
            request.correct_digit
        )

    db.commit()

    return {
        "message": "Feedback saved"
    }