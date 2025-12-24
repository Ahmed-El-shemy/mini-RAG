from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os
from app.helpers.config import get_settings, Settings
from app.controllers import DataController, ProjectController, ProcessController
from app.models.enums.response_signal import ResponseSignal
import logging
import aiofiles
from app.models.db_schemes.data_scheme import ProcessRequest
from app.models.db_schemes.data_chunk import DataChunk
from app.models.ProjectModel import ProjectModel
from app.models.ChunkModel import ChunkModel
logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(request:Request, project_id: str, file: UploadFile,
                app_settings:Settings = Depends(get_settings)):

    project_model = ProjectModel(
        db_client=request.app.state.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    is_valid , message = DataController().validate_upload_file(file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": message
            }
        )
    

    projct_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = DataController().generate_unique_file_path(
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
            "file_id":file_id,
            "project_id":str(project_id) 
        }   
    )


@data_router.post("/process/{project_id}")
async def process_endpoint(request:Request,project_id:str , process_request:ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap
    do_reset = process_request.do_reset

    project_model = ProjectModel(
        db_client=request.app.state.db_client
    )e

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    chunk_model = ChunkModel(
        db_client=request.app.state.db_client
    )

    if do_reset == 1:
        _ = await chunk_model.delete_chunks(project_id=project_id)
    
    process_controller = ProcessController(project_id=project_id)
    
    process_content = process_controller.get_file_content(file_id=file_id)
    
    file_chunks = process_controller.process_file_content(
        file_content=process_content,
        file_id=file_id,
        chunk_size=chunk_size,
        chunk_overlap=overlap_size
    )
    
    if process_content is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_PROCESSING_FAILED.value
            }
        )
    
    file_chunks_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id=project.id,
        )
             for chunk in file_chunks

    ]
   
    

    no_records =await chunk_model.insert_many_chunks(chunks=file_chunks_records)
     
    
    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records
        }
    )

    