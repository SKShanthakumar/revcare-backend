from sqlalchemy import Column, VARCHAR, Integer
from app.database import Base

class PaymentMethod(Base):
    """payment type data (online/Cash on delivery)"""
    __tablename__ = "payment_methods"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False)
    
    def __repr__(self):
        return f"<PaymentMethod(id='{self.id}', name='{self.name}')>"
    