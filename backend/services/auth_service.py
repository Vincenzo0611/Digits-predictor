from sqlalchemy.orm import Session

from backend.models.user import User

from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


def register_user(
    db: Session,
    email: str,
    password: str
):

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        return None

    user = User(
        email=email,
        password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(
    db: Session,
    email: str,
    password: str
):

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password
    ):
        return None

    token = create_access_token({
        "sub": user.email,
        "role": user.role
    })

    return token