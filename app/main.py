from fastapi import FastAPI ,APIRouter
from app.routes import basy
app = FastAPI()

app.include_router(basy.base_router)