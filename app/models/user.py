from sqlalchemy import Column, Integer, String, Enum

from app.core.database import Base
import enum



class UserRole(str, enum.Enum):
    admin = "admin"
    customer = "customer"



class User(Base):  
    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.customer, nullable=False)
      