import os
from fastapi import FastAPI
import motor.motor_asyncio


app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.college

@app.get("/")
async def root():
    return {"message": "ok"}
