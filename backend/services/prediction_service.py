import numpy as np
import uuid
import os

from backend.core.config import PROCESSED_DIR
from backend.ml.model_loader import model
from backend.ml.preprocess import preprocess_image


def predict_digit(image_path: str):

    processed_filename = f"{uuid.uuid4()}.png"

    processed_path = os.path.join(
        PROCESSED_DIR,
        processed_filename
    )

    processed_image = preprocess_image(
        image_path,
        save_processed_path=processed_path
    )

    predictions = model.predict(processed_image)

    predicted_digit = int(np.argmax(predictions))

    confidence = float(np.max(predictions))

    return {
        "digit": predicted_digit,
        "confidence": round(confidence, 4),
        "processed_image": processed_filename
    }