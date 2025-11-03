from fastapi import APIRouter
from . import admin, customer, mechanic, auth, car, address, service

router = APIRouter()
router.include_router(customer.router, prefix="/customers", tags=["Customers"])
router.include_router(admin.router, prefix="/admins", tags=["Admins"])
router.include_router(mechanic.router, prefix="/mechanics", tags=["Mechanics"])
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(car.router, prefix="/car", tags=["Cars"])
router.include_router(address.router, prefix="/address", tags=["Address"])
router.include_router(service.router, prefix="/services", tags=["Services"])
