"""
Testes (Pytest) para a nova implementação.
"""

import pytest
from app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as c:
        yield c


def test_root_healthcheck(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json == {"status": "ok"}


def test_list_users_initially_empty(client):
    r = client.get("/users/")
    assert r.status_code == 200
    assert r.json == []


def test_create_user_success(client):
    payload = {"name": "Alice", "age": 28}
    r = client.post("/users/", json=payload)
    assert r.status_code == 201
    assert r.json["name"] == "Alice"
    assert r.json["age"] == 28
    assert "id" in r.json


def test_create_user_invalid_payload(client):
    r = client.post("/users/", json={"name": "Sem idade"})
    assert r.status_code == 400
    assert r.json["error"] == "invalid payload"


def test_retrieve_existing_user(client):
    new_user = client.post("/users/", json={"name": "Bob", "age": 22}).json
    uid = new_user["id"]

    r = client.get(f"/users/{uid}")
    assert r.status_code == 200
    assert r.json["name"] == "Bob"
    assert r.json["age"] == 22


def test_retrieve_nonexistent_user(client):
    r = client.get("/users/9999")
    assert r.status_code == 404
    assert r.json["error"] == "user not found"
