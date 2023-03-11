from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def hello_word():
    return {"msg": "Hello World"}
