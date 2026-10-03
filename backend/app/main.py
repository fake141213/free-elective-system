import os

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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
        "https://frontend-ivory-zeta-42.vercel.app",
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


@app.get("/health/env")
def env_health():
    database_url = os.getenv("DATABASE_URL")

    return {
        "has_database_url": bool(database_url),
        "database_url_prefix": (
            database_url.split("://")[0]
            if database_url and "://" in database_url
            else None
        ),
    }