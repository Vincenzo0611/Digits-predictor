from fastapi import FastAPI

from backend.db.database import Base, engine

from backend.models.user import User
from backend.models.prediction import Prediction

from fastapi.staticfiles import StaticFiles

from backend.api.health import router as health_router
from backend.api.auth import router as auth_router
from backend.api.users import router as users_router
from backend.api.prediction import router as prediction_router
from backend.api.feedback import router as feedback_router
from backend.api.dashboard import router as dashboard_router

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Digit Recognition API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/processed",
    StaticFiles(directory="backend/uploads/processed"),
    name="processed"
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(prediction_router)
app.include_router(feedback_router)
app.include_router(dashboard_router)