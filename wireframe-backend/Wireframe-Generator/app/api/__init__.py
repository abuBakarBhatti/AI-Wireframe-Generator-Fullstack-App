from fastapi import APIRouter

from app.api.endpoints import wireframe

api_router = APIRouter()
api_router.include_router(wireframe.router, prefix="/wireframe", tags=["wireframe"])