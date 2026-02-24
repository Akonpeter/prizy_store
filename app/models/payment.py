from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base



class Payment(Base):
    __tablename__ = "payments"


    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    reference = Column(String, unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="Pending") # Pending 
    create_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("app.models.order.order", back_populates="payment", uselist=False)
    