import asyncio
import razorpay, hmac, hashlib
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.models import Booking
from app.core.config import settings

razorpay_client = razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))


async def create_razorpay_order(total: float):
    """
    Create a Razorpay order and return order details.
    
    Creates a payment order with the specified amount in INR.
    The amount is converted to paise (smallest currency unit) for Razorpay.
    
    Args:
        total: Total amount in rupees (float)
        
    Returns:
        dict: Razorpay order details including order_id
        
    Note:
        Runs the synchronous Razorpay client in an async thread to avoid blocking.
    """
    def _create():
        order_data = {
            "amount": int(float(total) * 100),     # amount in paise
            "currency": "INR"
        }
        return razorpay_client.order.create(order_data)
    
    # creating client is sync so run in async thread
    return await asyncio.to_thread(_create)


def verify_signature(order_id: str, payment_id: str, signature: str) -> bool:
    """
    Verify Razorpay payment signature.
    
    Verifies the payment signature sent by Razorpay to ensure the payment
    is authentic and hasn't been tampered with.
    
    Args:
        order_id: Razorpay order ID
        payment_id: Razorpay payment ID
        signature: Signature provided by Razorpay
        
    Returns:
        bool: True if signature is valid, False otherwise
    """
    msg = f"{order_id}|{payment_id}"
    generated = hmac.new(
        bytes(settings.razorpay_key_secret, "utf-8"),
        bytes(msg, "utf-8"),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(generated, signature)
