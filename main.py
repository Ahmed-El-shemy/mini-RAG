from fastapi import FastAPI ,APIRouter
from src.routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from src.helpers.config import get_settings

app = FastAPI()
@app.on_event("startup")
async def startup():
    settings = get_settings()
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_DATABASE]
    app.state.db_client = app.mongodb

@app.on_event("shutdown")
async def shutdown():
    app.mongodb_client.close()


app.include_router(base.base_router)
app.include_router(data.data_router)