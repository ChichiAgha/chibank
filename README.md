# Techbleat Global Bank — Kubernetes

This repository contains a production-style deployment of the complete banking application with Helm, Kubernetes health and capacity controls, Prometheus metrics and alerts, Grafana dashboards, Loki logging, and operational runbooks.

## quick start

```bash
minikube start --cpus=4 --memory=8192
minikube addons enable ingress
minikube addons enable metrics-server
./scripts/install-observability.sh
helm upgrade --install bleatbank charts/bleatbank \
  --namespace banking --create-namespace \
  --values charts/bleatbank/values-dev.yaml \
  --wait --timeout 15m
```

The default chart references the instrumented `chigoldd/chibank-*` images tagged `v1.1.0`. Publish a new immutable version using [the image guide](docs/image-build-and-push.md) whenever application instrumentation changes. The full procedure, access commands, alert testing, and Slack setup are in [the deployment guide](docs/deployment.md).

Capstone assets:

- Helm deployment: `charts/bleatbank/`
- Operations and business dashboards: `dashboards/`
- Seven Prometheus alerts: `alerts/` and the Helm chart
- Alert runbooks: `runbooks/`
- Prometheus, Grafana, Loki and Alloy configuration: `monitoring/`
- Architecture: `docs/architecture.md`

Live screenshots and the demo-video link cannot be generated honestly from source code alone. Capture those from the running environment and place them under `screenshots/` before submission.

---

# Application development reference

A microservices-based banking platform built with Python (FastAPI), Java (Spring Boot), PostgreSQL, Redis, and Apache Kafka. The system handles user management, financial transactions, and activity logging through independent, event-driven services.

---

## Architecture Overview

<iframe src="architectural-diagram.html" width="100%" height="520" frameborder="0" style="border:none;border-radius:8px;"></iframe>

> **Note:** The interactive diagram above renders in local viewers (VS Code preview, etc.). On GitHub, iframes are blocked — use the static image below instead.

![Architecture Diagram](architectural-diagram.png)

```
                         ┌──────────────────┐
                         │   Frontend (3000) │
                         └────────┬─────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
   ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐
   │  User Service   │  │Transaction Service│  │Activity Service  │
   │  FastAPI :8000  │  │ Spring Boot :8080 │  │  FastAPI :8001   │
   └────────┬────────┘  └────────┬─────────┘  └────────┬─────────┘
            │                    │                       │
            ▼                    ▼                       ▲
   ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐
   │   PostgreSQL    │  │      Redis       │  │      Kafka       │
   │   Port 5432     │  │    Port 6379     │  │    Port 9092     │
   └─────────────────┘  └──────────────────┘  └──────────────────┘
```

### Services

| Service | Language | Port | Responsibility |
|---------|----------|------|----------------|
| user-service | Python / FastAPI | 8000 | User registration and account creation |
| transaction-service | Java / Spring Boot | 8080 | Deposits, withdrawals, transfers, balance queries |
| activity-service | Python / FastAPI | 8001 | Activity log via Kafka consumer |

### Infrastructure

| Component | Version | Port | Purpose |
|-----------|---------|------|---------|
| PostgreSQL | 15 | 5432 | Persistent data store |
| Redis | 7 | 6379 | Balance caching |
| Apache Kafka | 8.1.1 | 9092 | Event streaming between services |

---

## Prerequisites

- [Docker](https://www.docker.com/get-started) 20.10+
- [Docker Compose](https://docs.docker.com/compose/install/) v2+

No local installations of Python, Java, or any database are needed — everything runs inside containers.

---

## Running Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd techbleat-global-bank-backend
```

### 2. Start all services

```bash
docker compose up --build
```

This command will:
- Build Docker images for all three services
- Start PostgreSQL, Redis, and Kafka
- Run the database initialisation script (`db-init/init.sql`)
- Start all three application services

### 3. Verify services are running

```bash
curl http://localhost:8000/health   # User Service
curl http://localhost:8080/health   # Transaction Service
curl http://localhost:8001/health   # Activity Service
```

### 4. Stop all services

```bash
docker compose down
```

To also remove volumes (wipes database data):

```bash
docker compose down -v
```

---

## API Reference

### User Service — `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/users` | Create a new user and bank account |
| GET | `/users` | List all users |

**Create User**

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"id": "u001", "full_name": "Jane Doe", "email": "jane@example.com"}'
```

Creating a user automatically initialises a bank account with a zero balance.

---

### Transaction Service — `http://localhost:8080`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/transactions/deposit` | Deposit funds |
| POST | `/transactions/withdraw` | Withdraw funds |
| POST | `/transactions/transfer` | Transfer between accounts |
| GET | `/balance/{userId}` | Get account balance (Redis-cached) |
| GET | `/transactions/{userId}` | Get last 20 transactions |

The user ID is passed via the `X-User-Id` request header for all write operations.

**Deposit**

```bash
curl -X POST http://localhost:8080/transactions/deposit \
  -H "Content-Type: application/json" \
  -H "X-User-Id: u001" \
  -d '{"amount": 500.00}'
```

**Withdraw**

```bash
curl -X POST http://localhost:8080/transactions/withdraw \
  -H "Content-Type: application/json" \
  -H "X-User-Id: u001" \
  -d '{"amount": 100.00}'
```

**Transfer**

```bash
curl -X POST http://localhost:8080/transactions/transfer \
  -H "Content-Type: application/json" \
  -H "X-User-Id: u001" \
  -d '{"toUserId": "u002", "amount": 50.00, "reference": "rent payment"}'
```

**Check Balance**

```bash
curl http://localhost:8080/balance/u001
```

---

### Activity Service — `http://localhost:8001`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/activities/{userId}` | Get last 20 activity log entries |

**Get Activities**

```bash
curl http://localhost:8001/activities/u001
```

Activities are written automatically when the Activity Service consumes transaction events from the Kafka topic `banking-transactions`.

---

## Environment Variables

Runtime values are loaded from environment variables. For local Docker Compose, copy `.env.example` to `.env` and provide real values before starting the stack.

### User Service & Activity Service

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://<db-user>:<db-password>@postgres:5432/<db-name>` | PostgreSQL connection string |
| `FRONTEND_ORIGIN` | `http://localhost:3000` | CORS allowed origin |

### Transaction Service

| Variable | Default | Description |
|----------|---------|-------------|
| `SPRING_DATASOURCE_URL` | `jdbc:postgresql://postgres:5432/<db-name>` | JDBC connection URL |
| `SPRING_DATASOURCE_USERNAME` | `<db-user>` | Database username |
| `SPRING_DATASOURCE_PASSWORD` | `<db-password>` | Database password |
| `KAFKA_BOOTSTRAP_SERVERS` | `kafka:29092` | Kafka broker address |
| `REDIS_HOST` | `redis` | Redis hostname |
| `REDIS_PORT` | `6379` | Redis port |
| `SERVER_PORT` | `8080` | Application port |

### Activity Service

| Variable | Default | Description |
|----------|---------|-------------|
| `KAFKA_BOOTSTRAP_SERVERS` | `kafka:29092` | Kafka broker address |

---

## Database Schema

Initialised automatically on first startup via `db-init/init.sql`.

```
users          — id, full_name, email, created_at
accounts       — user_id (FK), balance, updated_at
transactions   — id, user_id, transaction_type, amount, reference, created_at
activities     — id, user_id, activity_type, description, created_at
```

---

## Event Flow

1. A client calls the Transaction Service (deposit / withdraw / transfer).
2. The Transaction Service writes to PostgreSQL and publishes an event to the Kafka topic `banking-transactions`.
3. The Activity Service consumes the Kafka event and writes an entry to the `activities` table.
4. Balance reads are served from Redis cache; the cache is updated on each write.

---

## Running Individual Services Locally (without Docker)

### User Service / Activity Service (Python)

```bash
cd user-service           # or activity-service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DATABASE_URL=postgresql://<db-user>:<db-password>@localhost:5432/<db-name> \
  uvicorn app.main:app --reload --port 8000
```

### Transaction Service (Java)

```bash
cd transaction-service
./mvnw spring-boot:run
```

Requires Java 17+ and Maven installed locally. Infrastructure (PostgreSQL, Redis, Kafka) must be running separately.

---

## CORS

All services are configured to accept cross-origin requests from `http://localhost:3000` and `http://127.0.0.1:3000` to support the companion React frontend.
