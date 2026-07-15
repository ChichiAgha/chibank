import importlib


def load_app(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://banking_user:banking_password@localhost:5432/bankingdb")
    monkeypatch.setenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    return importlib.import_module("app.main")


def test_health_returns_ok(monkeypatch):
    service = load_app(monkeypatch)

    assert service.health() == {"status": "ok"}
