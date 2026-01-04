from fastapi import FastAPI, APIRouter, Depends
from src.helpers.config import get_settings, Settings

base_router = APIRouter()

@base_router.get("/")
async def welcome(app_setings:Settings = Depends(get_settings)):
    app_name = app_setings.APP_NAME
    app_version = app_setings.APP_VERSION
    return {
        "app_name": app_name,
        "app_version": app_version,
    }
