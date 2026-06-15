from fastapi import APIRouter
from fastapi import Depends

from backend.models.user import User

from backend.api.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }