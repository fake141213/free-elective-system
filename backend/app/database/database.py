import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool


# =========================
# Database URL
# =========================

DATABASE_URL = os.getenv("DATABASE_URL")


# =========================
# Local development
# =========================

# ถ้าไม่มี DATABASE_URL ให้ใช้ SQLite เหมือนเดิม
if not DATABASE_URL:
    BASE_DIR = Path(__file__).resolve().parents[2]
    DATABASE_PATH = BASE_DIR / "data" / "free_elective.db"
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# =========================
# PostgreSQL URL
# =========================

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+psycopg://",
        1,
    )

elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1,
    )


# =========================
# Engine
# =========================

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False
        },
    )

else:
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
        pool_pre_ping=True,
    )


# =========================
# Session
# =========================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# =========================
# Base
# =========================

Base = declarative_base()


# =========================
# Dependency
# =========================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()