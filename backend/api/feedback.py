from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from pydantic import BaseModel

from sqlalchemy.orm import Session

from backend.db.database import get_db

from backend.models.prediction import Prediction

from backend.api.dependencies import get_current_user

from backend.core.s3 import delete_image


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

    prediction.is_correct = (
        request.is_correct
    )

    if request.is_correct:

        try:

            if prediction.image_url:

                delete_image(
                    prediction.image_url
                )

            if prediction.processed_image_url:

                delete_image(
                    prediction.processed_image_url
                )

        except Exception as e:

            print(
                f"S3 delete error: {e}"
            )

        db.delete(prediction)

    else:

        prediction.correct_digit = (
            request.correct_digit
        )

    db.commit()

    return {
        "message": "Feedback saved"
    }