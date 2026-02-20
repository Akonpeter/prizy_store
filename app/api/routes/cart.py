from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.product import product
from app.core.security import get_current_user
from app.schemas.cart import  AddToCart




router = APIRouter(prefix="/cart", tags=["Cart"])



def get_db():
    db = SessionLocal()
    try:
        yield
    finally:
        db.close()




     # View Cart
@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)

):

    cart = db.query(cart).filter(cart.user_id == current_user.id).first()
    if not cart:
        return{"items": [],  "total": 0}
    

    total = 0
    cart_data = []


for item in cart.items:
    product = db.query(product).filter(product.id == item.product_id).first()
    if product:
        subtotal = product.price * item.quantity
        total  += subtotal
        
        
    cart_data.append({
        "product_id": product.id,
        "name": product.name,
        "price": product.price,
        "quantity": item.quantity,
        "subtotal": subtotal

        })   
    
return {"items": cart_data, "total": total} 


# Add to Cart
@router.post("/add")
def add_to_cart(
    data: AddToCart,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
    
):
    
    product = db.query(product).filter(product.id ==data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    
    if product.stock_quantity < data.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    
    cart = db.query(Cart).filter(Cart.user_id == get_current_user.id).first()

    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)


    existing_item = db.query(CartItem).filter(
        cartItem.cart_id == cart.id,
        CartItem.product_id == data.product_id
    ).first()


    if existing_item:
        existing_item.quantity += data.quantity
    else:
        new_item = CartItem(
            cart_id=cart.id,
            product_id=data.product_id,
            quantity=data.quantity
        ) 
        db.add(new_item)
    db.commit()
    return {"message": "Item added to cart"}


# Remove item from cart

@router.delete("/{product_id}")
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)

):
    cart = db.query(Cart).filter(Cart.user_id == get_current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found ")
    
    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()


    if not item:
        raise HTTPException(status_code=404, detail="Item not in found in cart")
    

    db.delete(item)
    db.commit()


    return {"message": "Item removed"}
    
    
    

    




    