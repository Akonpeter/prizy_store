from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import session
from app.core.database import SessionLocal
from app.models.cart import Cart
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.core.security import get_current_user, require_admin
from app.schemas.order import OrderResponse


router = APIRouter(prefix="/orders", tags=["Orders"])



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Checkout

@router.post("/checkout", response_model=OrderResponse)
def checkout(
    db: session = Depends(get_db),
    current_user=Depends(get_current_user)

):

    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    

    total = 0
    order = Order(user_id=current_user.id, total_amount=0)
    db.add(order)
    db.flush()    # get order.id before commit


    for item in cart.items:
        product = db.query(product).filter(product.id == item.product_id).first()

        if not product or product.stock_quantity < item.quantity:    
           product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product or product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")

        subtotal = product.price * item.quantity
        total += subtotal

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price_at_purchase=product.price
        )
        db.add(order_item)

        # Deduct stock
        
        product.stock_quantity -= item.quantity

    order.total_amount = total

    # Clear cart
    db.query(Cart).filter(Cart.user_id == current_user.id).delete()

    db.commit()
    db.refresh(order)

    return order


# 📜 Customer Order History
@router.get("/my-orders", response_model=list[OrderResponse])
def get_my_orders(
    db: session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Order).filter(Order.user_id == current_user.id).all()


# 🛠 Admin: View All Orders
@router.get("/", response_model=list[OrderResponse])
def get_all_orders(
    db: session = Depends(get_db),
    admin=Depends(require_admin)
):
    return db.query(Order).all()


# 🛠 Admin: Update Order Status
@router.put("/{order_id}/status")
def update_order_status(
    order_id: int,
    status: str,
    db: session = Depends(get_db),
    admin=Depends(require_admin)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    db.commit()

    return {"message": "Order status updated"}