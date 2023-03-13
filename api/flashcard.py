from typing import Optional
from fastapi import APIRouter, Body, Request, HTTPException, status
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import os

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


@router.get("/flashcards/{id}", response_description="Get a single flashcard")
async def show_flashcards(id: str, request: Request):
    if (flashcard := await request.app.mongodb["flashcards"].find_one({"_id": id})) is not None:
        return flashcard

    raise HTTPException(status_code=404, detail=f"Flashcard {id} not found")


@router.post("/flashcards", response_description="Create a flashcard",
             response_model=FlashcardModel)
async def create_flashcard(request: Request, flashcard: FlashcardModel = Body(...)):
    flashcard = jsonable_encoder(flashcard)
    new_flashcard = await request.app.mongodb["flashcards"].insert_one(flashcard)
    created_flashcard = await request.app.mongodb["flashcards"].find_one(
        {"_id": new_flashcard.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_flashcard)


@router.put("/flashcards/{id}", response_description="Update a flashcard")
async def update_flashcard(id: str, request: Request, flashcard: UpdateFlashcard = Body(...)):
    flashcard = {k: v for k, v in flashcard.dict().items() if v is not None}

    await request.app.mongodb["flashcards"].update_one(
        {"_id": id},
        {"$set": flashcard}
    )

    if (
        existing_flashcard := await request.app.mongodb["flashcards"].find_one({"_id": id})
    ) is not None:
        return existing_flashcard

    raise HTTPException(status_code=404, detail=f"Flashcard {id} not found")


@router.delete("/flashcards/{id}", response_description="Delete a flashcard")
async def delete_flashcard(id: str, request: Request):
    delete_result = await request.app.mongodb["flashcards"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Flashcard {id} not found")
