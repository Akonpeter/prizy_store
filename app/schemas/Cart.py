from pydantic import BaseModel




class AddToCart(BaseModel):
    product_id: int
    quantity: int



class CartItemResponse(BaseModel):
    product_id: int
    quantity: int


class Config:
    orm_mode = True
            