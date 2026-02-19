from pydantic import BaseModel





class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock_quantity: int
    image_url: str | None = None


class ProductResponse(ProductCreate):
    id: int


class Config:
    orm_mode = True        