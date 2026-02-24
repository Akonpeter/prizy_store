from pydantic import BaseModel
from datetime import datetime



class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float



    class Config:
        orm_mode = True




class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: str   
    created_at: datetime
    items: list[OrderItemResponse]


    class Config:
        orm_mode = True     
