from fastapi import APIRouter

from app.api.routes import router as workflow_router

api_router = APIRouter()
api_router.include_router(workflow_router, tags=["Gate-pass workflow"])
