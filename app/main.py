import os
from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.api import flashcard, helloword

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(os.environ["DB_URL"])
    app.mongodb = app.mongodb_client[os.environ["DB_NAME"]]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

routers = [
    flashcard.router,
    helloword.router,
]

for router in routers:
    app.include_router(router)


def main():
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )


if __name__ == "__main__":
    main()
