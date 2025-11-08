import asyncio
import razorpay, hmac, hashlib
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.models import Booking
from app.core.config import settings

razorpay_client = razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))


async def create_razorpay_order(total: float):
    """Create Razorpay order and return details."""
    def _create():
        order_data = {
            "amount": total * 100,     # amount in paise
            "currency": "INR"
        }
        return razorpay_client.order.create(order_data)
    
    # creating client is sync so run in async thread
    return await asyncio.to_thread(_create)


def verify_signature(order_id: str, payment_id: str, signature: str) -> bool:
    """Verify Razorpay signature."""
    msg = f"{order_id}|{payment_id}"
    generated = hmac.new(
        bytes(settings.razorpay_key_secret, "utf-8"),
        bytes(msg, "utf-8"),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(generated, signature)
