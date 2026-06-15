import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"

UPLOAD_DIR = "backend/uploads"
PROCESSED_DIR = "backend/uploads/processed"