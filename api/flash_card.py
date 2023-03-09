from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class CreateFlashCard(BaseModel):
    frontSide: str
    backSide: str
