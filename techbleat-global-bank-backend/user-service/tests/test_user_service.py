import importlib


def load_app(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://banking_user:banking_password@localhost:5432/bankingdb")
    return importlib.import_module("app.main")


def test_health_returns_ok(monkeypatch):
    service = load_app(monkeypatch)

    assert service.health() == {"status": "ok"}


def test_user_create_normalizes_valid_input(monkeypatch):
    service = load_app(monkeypatch)

    user = service.UserCreate(id="user1", full_name="Alice Example", email="alice@example.com")

    assert user.id == "user1"
    assert user.full_name == "Alice Example"
    assert user.email == "alice@example.com"
