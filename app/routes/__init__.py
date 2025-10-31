from fastapi import APIRouter
from . import admin, customer, mechanic, auth, car

router = APIRouter()
router.include_router(customer.router, prefix="/customers", tags=["Customers"])
router.include_router(admin.router, prefix="/admins", tags=["Admins"])
router.include_router(mechanic.router, prefix="/mechanics", tags=["Mechanics"])
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(car.router, prefix="/car", tags=["Cars"])
