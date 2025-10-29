from fastapi import APIRouter
from . import admin, customer

router = APIRouter()
router.include_router(customer.router, prefix="/customers", tags=["Customers"])
router.include_router(admin.router, prefix="/admins", tags=["Admins"])