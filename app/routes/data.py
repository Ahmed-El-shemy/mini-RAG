from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from app.helpers.config import get_settings, Settings
from app.controllers import DataController, ProjectController
from .schemes.data_scheme import ResponseSignal
import os
import logging
import aiofiles

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                app_settings:Settings = Depends(get_settings)):

    is_valid , message = DataController.validate_upload_file(file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": message
            }
        )
    

    projct_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = DataController().generate_unique_filename(
        orig_file_name=file.filename,
        project_id=project_id
    )


    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": "FILE_UPLOAD_FAILED"
            }
        )
    
    return JSONResponse (
        content={
            "signal":ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id":file_id
        }   
    )