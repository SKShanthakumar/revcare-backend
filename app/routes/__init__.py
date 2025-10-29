from fastapi import APIRouter
from . import admin, customer, mechanic

router = APIRouter()
router.include_router(customer.router, prefix="/customers", tags=["Customers"])
router.include_router(admin.router, prefix="/admins", tags=["Admins"])
router.include_router(mechanic.router, prefix="/mechanics", tags=["Mechanics"])
