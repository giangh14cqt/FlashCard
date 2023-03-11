from fastapi.testclient import TestClient
from main import app
from motor.motor_asyncio import AsyncIOMotorClient
import os
# import pytest

client = TestClient(app)

client.app.mongodb_client = AsyncIOMotorClient(os.environ["DB_URL"])
client.app.mongodb = app.mongodb_client[os.environ["DB_NAME"]]


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_create_flashcard():
    response = client.get("/flashcards")
    assert response.status_code == 200
    assert len(response.json()) == 3
