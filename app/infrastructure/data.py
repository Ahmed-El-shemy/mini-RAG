from fastapi import FastAPI, APIRouter, Depends, UploadFile
from .config import get_settings, Settings
from .Datacontroller import DataController

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(projct_id:str,file:UploadFile,
app_settings:Settings = Depends(get_settings)):
