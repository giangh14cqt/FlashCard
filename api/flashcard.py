from typing import List, Optional
from fastapi import APIRouter, Body, Request, HTTPException, status
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
import uuid

router = APIRouter()


class FlashcardModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    front_side: str = Field(...)
    back_side: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "front_side": "Hola",
                "back_side": "Hello",
            }
        }


class UpdateFlashcard(BaseModel):
    front_side: Optional[str]
    back_side: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "front_side": "Hola",
                "back_side": "Hello",
            }
        }


@router.get("/flashcards", response_description="List all flashcards")
async def list_flashcards(request: Request):
    flashcards = []
    for doc in await request.app.mongodb["flashcards"].find().to_list(length=100):
        flashcards.append(doc)
    return flashcards


@router.post("/flashcards", response_description="Create a flashcard", response_model=FlashcardModel)
async def create_flashcard(request: Request, flashcard: FlashcardModel = Body(...)):
    flashcard = jsonable_encoder(flashcard)
    new_flashcard = await request.app.mongodb["flashcards"].insert_one(flashcard)
    created_flashcard = await request.app.mongodb["flashcards"].find_one(
        {"_id": new_flashcard.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_flashcard)
