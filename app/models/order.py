from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from sqlalchemy.orm import relationship



class Order(Base):
    __tablename__ = "orders"



    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)



    items = relationship("OrderItem", back_populates="order", cascade="all, delete")



class OrderItem(Base):
    __tablename__ = "order_items"


    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price_at_purchase = Column(Float)


    order = relationship("Order", back_populates="items")   



    # Linking payment with order

    class Order(Base):
        __tablename__ = "orders"
        # existing fields..


        payment = relationship("app.models.payment.payment", back_populates="order", uselist=False)
