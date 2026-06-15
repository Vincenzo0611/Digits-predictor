from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship

from backend.db.database import Base


class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)

    image_path = Column(String, nullable=False)

    processed_image_path = Column(
        String,
        nullable=False
    )

    predicted_digit = Column(
        Integer,
        nullable=False
    )

    confidence = Column(
        Float,
        nullable=False
    )

    is_correct = Column(Boolean, nullable=True)

    correct_digit = Column(
        Integer,
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship("User")