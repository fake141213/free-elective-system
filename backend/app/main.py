from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.suggestions import router as suggestions_router
from app.api.dashboard import router as dashboard_router
from app.api.auth import router as auth_router

from app.database.database import Base, engine
from app.database import models


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Free Elective System API",
    description="API สำหรับระบบเสนอและวิเคราะห์ความต้องการรายวิชาเสรีของนักศึกษา",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Free Elective System API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


app.include_router(
    suggestions_router,
    prefix="/api"
)


app.include_router(
    dashboard_router,
    prefix="/api"
)


app.include_router(
    auth_router,
    prefix="/api"
)