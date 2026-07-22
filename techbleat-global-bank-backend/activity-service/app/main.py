import json
import os
import threading
import time
import logging
from datetime import datetime, timezone

from confluent_kafka import Consumer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from prometheus_client import Counter, Gauge
from prometheus_fastapi_instrumentator import Instrumentator

DATABASE_URL = os.getenv("DATABASE_URL")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required")

engine = create_engine(f"postgresql+psycopg2://{DATABASE_URL.split('://', 1)[1]}")

app = FastAPI(title="Techbleat Global Bank - Activity Service")


class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": record.levelname,
                "service": "activity-service",
                "message": record.getMessage(),
            }
        )


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("activity-service")
logger.handlers = [handler]
logger.setLevel(logging.INFO)
logger.propagate = False

activities_consumed = Counter(
    "bank_activity_events_consumed_total",
    "Kafka transaction events successfully persisted by the activity service",
    ["event_type"],
)
kafka_consumer_errors = Counter(
    "bank_activity_consumer_errors_total",
    "Kafka consumer or activity persistence errors",
)
active_users_5m = Gauge(
    "bank_active_users_5m",
    "Distinct users with transaction activity during the last five minutes",
)
recent_user_activity = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)


def kafka_consumer_loop():
    consumer = None
    while consumer is None:
        try:
            consumer = Consumer(
                {
                    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
                    "group.id": "activity-service-group",
                    "auto.offset.reset": "earliest",
                }
            )
            consumer.subscribe(["banking-transactions"])
        except Exception as exc:
            kafka_consumer_errors.inc()
            logger.warning("kafka_connect_failed error=%s", exc)
            time.sleep(3)

    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                kafka_consumer_errors.inc()
                logger.warning("kafka_message_error error=%s", msg.error())
                continue

            event = json.loads(msg.value().decode("utf-8"))
            user_id = event.get("userId", "unknown")
            activity_type = event.get("eventType", "UNKNOWN")
            amount = event.get("amount", 0)
            description = f"{activity_type} of {amount} by {user_id}"

            with engine.begin() as conn:
                conn.execute(
                    text(
                        '''
                        INSERT INTO activities (user_id, activity_type, description)
                        VALUES (:user_id, :activity_type, :description)
                        '''
                    ),
                    {
                        "user_id": user_id,
                        "activity_type": activity_type,
                        "description": description,
                    },
                )
            activities_consumed.labels(event_type=activity_type).inc()
            now = time.time()
            recent_user_activity[user_id] = now
            cutoff = now - 300
            for inactive_user in [
                key for key, last_seen in recent_user_activity.items() if last_seen < cutoff
            ]:
                recent_user_activity.pop(inactive_user, None)
            active_users_5m.set(len(recent_user_activity))
            logger.info("activity_persisted user_id=%s event_type=%s", user_id, activity_type)
        except Exception as exc:
            kafka_consumer_errors.inc()
            logger.exception("activity_consumer_failed error=%s", exc)
            time.sleep(1)


@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=kafka_consumer_loop, daemon=True)
    thread.start()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/activities/{user_id}")
def get_activities(user_id: str):
    with engine.begin() as conn:
        rows = conn.execute(
            text(
                '''
                SELECT id, user_id, activity_type, description, created_at
                FROM activities
                WHERE user_id = :user_id
                ORDER BY created_at DESC
                LIMIT 20
                '''
            ),
            {"user_id": user_id},
        ).mappings().all()
        return [dict(row) for row in rows]
