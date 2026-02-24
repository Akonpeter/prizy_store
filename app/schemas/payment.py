from pydantic import BaseModel
from datetime import datetime



class PaymentRequest(BaseModel):
    order_id: int



class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    status: str
    created_at: datetime


class Config:
            orm_mode = True