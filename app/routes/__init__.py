from fastapi import APIRouter
from . import admin, customer, mechanic, auth, car, address, service, utility, bookings, payment, payment_demo, content, gst, query, notification

router = APIRouter()
router.include_router(customer.router, prefix="/customers", tags=["Customers"])
router.include_router(admin.router, prefix="/admins", tags=["Admins"])
router.include_router(mechanic.router, prefix="/mechanics", tags=["Mechanics"])
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(car.router, prefix="/car", tags=["Cars"])
router.include_router(address.router, prefix="/address", tags=["Address"])
router.include_router(service.router, prefix="/services", tags=["Services"])
router.include_router(utility.router, prefix="/utils", tags=["Utilities"])
router.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
router.include_router(payment.router, prefix="/payment", tags=["Payment"])
router.include_router(payment_demo.router, prefix="/payment_demo")
router.include_router(content.router, prefix="/content", tags=["Content Management"])
router.include_router(gst.router, prefix="/gst", tags=["GST"])
router.include_router(query.router, prefix="/queries", tags=["Queries"])
router.include_router(notification.router, prefix="/notification", tags=["Notification"])
