from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field
from py_object_id import PyObjectId
from bson import ObjectId

router = APIRouter()


class FlashCardModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
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


class UpdateFlashCard(BaseModel):
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


@router.get("/", response_description="List all flashcards", response_model=List[FlashCardModel])
async def list_flash_cards():
    pass