from fastapi import APIRouter
from app.routes import router

router_v1 = APIRouter()
router_v1.include_router(router)
