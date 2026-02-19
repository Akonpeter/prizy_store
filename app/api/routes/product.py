from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.product import product
from app.schemas.product import ProductCreate, ProductResponse
from app.core.security import get_current_user, require_admin


router = APIRouter(prefix="/products", tags=["product"])



def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()


# Public: View all products

@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends (get_db)):
    return db.query(Product).all()


#  Admin: Create product

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    
    new_product = Product(**product.dict())



    db.add(new_product)
    db.commit
    db.refresh(new_product)


    return new_product



# Admin: Delete product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    
    Product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}   
    