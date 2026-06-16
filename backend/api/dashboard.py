from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.db.database import get_db

from backend.models.prediction import Prediction
from backend.models.user import User

from backend.api.dependencies import get_current_user

from backend.core.s3 import delete_image


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = db.query(Prediction)

    if current_user.role != "admin":

        query = query.filter(
            Prediction.user_id == current_user.id
        )

    predictions = query.all()

    return [
        {
            "id": prediction.id,

            "prediction":
                prediction.predicted_digit,

            "confidence":
                prediction.confidence,

            "is_correct":
                prediction.is_correct,

            "correct_digit":
                prediction.correct_digit,

            "image_url":
                prediction.image_url,

            "processed_image_url":
                prediction.processed_image_url,

            "user_id":
                prediction.user_id,

            "user_email":
                prediction.user.email,
        }

        for prediction in predictions
    ]


@router.delete("/{prediction_id}")
def delete_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    prediction = (
        db.query(Prediction)
        .filter(
            Prediction.id == prediction_id
        )
        .first()
    )

    if not prediction:

        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    is_admin = (
        current_user.role == "admin"
    )

    is_owner = (
        prediction.user_id == current_user.id
    )

    if not is_admin and not is_owner:

        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

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

    db.commit()

    return {
        "message": "Prediction deleted"
    }