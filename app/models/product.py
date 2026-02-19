from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base





class product(Base):
    __tablename__ = "products"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    image_url = Column(String, nullable=True)
    

