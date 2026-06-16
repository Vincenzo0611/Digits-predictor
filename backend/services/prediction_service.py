import cv2
import numpy as np

from backend.ml.model_loader import model
from backend.ml.preprocess import preprocess_image


def bytes_to_image(file_bytes):

    np_array = np.frombuffer(
        file_bytes,
        np.uint8
    )

    img = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    return img


def predict_digit(file_bytes):

    img = bytes_to_image(file_bytes)

    processed_image, visual_image = preprocess_image(
        img,
        return_visual=True
    )

    predictions = model.predict(processed_image)

    predicted_digit = int(
        np.argmax(predictions)
    )

    confidence = float(
        np.max(predictions)
    )

    _, buffer = cv2.imencode(
        ".png",
        visual_image
    )

    processed_bytes = buffer.tobytes()

    return {
        "digit": predicted_digit,
        "confidence": round(confidence, 4),
        "processed_bytes": processed_bytes
    }