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
    response = client.post(
        "/flashcards",
        json={"front_side": "Xin chao", "back_side": "Hello"})
    assert response.status_code == 201
    obj = response.json()
    assert obj["front_side"] == "Xin chao"
    assert obj["back_side"] == "Hello"
