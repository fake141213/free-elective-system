import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool


# =========================
# Database URL
# =========================

DATABASE_URL = os.getenv("DATABASE_URL")

print("===== DATABASE DEBUG =====")
print("DATABASE_URL exists:", bool(DATABASE_URL))

if DATABASE_URL:
    print(
        "DATABASE_URL prefix:",
        DATABASE_URL.split("://")[0]
    )
else:
    print("DATABASE_URL is NOT SET")


# =========================
# Local development
# =========================

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


print(
    "Database driver:",
    DATABASE_URL.split("://")[0]
)


# =========================
# Engine
# =========================

try:

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

    print("Database engine created successfully")

except Exception as e:

    print("DATABASE ENGINE ERROR:")
    print(type(e).__name__)
    print(str(e))

    raise


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