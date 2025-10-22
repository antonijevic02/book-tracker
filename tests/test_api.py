import os
import pytest
from app import app
from models import Base, engine, SessionLocal, Book

@pytest.fixture(autouse=True)
def setup_database():
    """Recreate database tables before each test for a clean state."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """Flask test client."""
    app.testing = True
    return app.test_client()


def test_health(client):
    """Check health endpoint."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_create_book(client):
    """Create a book and verify it exists."""
    resp = client.post("/books", json={"title": "1984", "author": "Orwell"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["title"] == "1984"
    assert "id" in data

    # verify via GET
    resp_get = client.get("/books")
    data_get = resp_get.get_json()
    assert len(data_get) == 1
    assert data_get[0]["title"] == "1984"


def test_update_book(client):
    """Create then update a book."""
    client.post("/books", json={"title": "Old Title", "author": "John"})
    resp = client.put("/books/1", json={"title": "New Title"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["title"] == "New Title"

    # verify persisted change
    resp_get = client.get("/books")
    data_get = resp_get.get_json()
    assert data_get[0]["title"] == "New Title"


def test_delete_book(client):
    """Create then delete a book."""
    client.post("/books", json={"title": "Delete Me", "author": "X"})
    resp_del = client.delete("/books/1")
    assert resp_del.status_code == 200
    assert resp_del.get_json()["message"] == "Deleted"

    # verify deletion
    resp_get = client.get("/books")
    data_get = resp_get.get_json()
    assert data_get == []
