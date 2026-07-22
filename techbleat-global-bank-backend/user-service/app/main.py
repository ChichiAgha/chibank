import os
import logging
import json
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, text
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator

DATABASE_URL = os.getenv("DATABASE_URL")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required")

engine = create_engine(f"postgresql+psycopg2://{DATABASE_URL.split('://', 1)[1]}")

app = FastAPI(title="Techbleat Global Bank - User Service")


class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": record.levelname,
                "service": "user-service",
                "message": record.getMessage(),
            }
        )


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("user-service")
logger.handlers = [handler]
logger.setLevel(logging.INFO)
logger.propagate = False

users_registered = Counter(
    "bank_users_registered_total",
    "Total number of successfully registered bank users",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)


class UserCreate(BaseModel):
    id: str
    full_name: str
    email: EmailStr


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/users")
def create_user(user: UserCreate):
    with engine.begin() as conn:
        existing = conn.execute(
            text("SELECT id FROM users WHERE id = :id OR email = :email"),
            {"id": user.id, "email": user.email},
        ).fetchone()

        if existing:
            raise HTTPException(status_code=400, detail="User ID or email already exists")

        conn.execute(
            text(
                '''
                INSERT INTO users (id, full_name, email)
                VALUES (:id, :full_name, :email)
                '''
            ),
            {"id": user.id, "full_name": user.full_name.title(), "email": user.email},
        )

        conn.execute(
            text(
                '''
                INSERT INTO accounts (user_id, balance)
                VALUES (:user_id, 0)
                '''
            ),
            {"user_id": user.id},
        )

    users_registered.inc()
    logger.info("user_registered user_id=%s", user.id)
    return {"message": "User created successfully", "user_id": user.id}


@app.get("/users")
def list_users():
    with engine.begin() as conn:
        rows = conn.execute(
            text(
                '''
                SELECT id, full_name, email, created_at
                FROM users
                ORDER BY created_at DESC
                '''
            )
        ).mappings().all()
        return [dict(row) for row in rows]
