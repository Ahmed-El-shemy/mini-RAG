from fastapi import FastAPI, APIRouter, Depends, UploadFile,status
from app.helpers.config import get_settings,Settings
from app.controllers import ProjectController,DataController

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(projct_id:str,file:UploadFile,
                app_settings:Settings = Depends(get_settings)):

    is_valid , message = DataController.validate_upload_file(file)

    if not is_valid:
        return JSONResponse{
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
                }
             
        }

    projct_dir_path = ProjectController().get_project_path(projct_id=projct_id)
