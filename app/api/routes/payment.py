from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from random import randint
from app.core.database import SessionLocal
from app.models.order import Order
from app.models.payment import Payment
from app.core.security import get_current_user
from app.schemas.payment import PaymentRequest, PaymentResponse

router = APIRouter(prefix="/payments", tags=["Payments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 💳 Simulate payment
@router.post("/", response_model=PaymentResponse)
def make_payment(
    payment_request: PaymentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == payment_request.order_id,
                                   Order.user_id == current_user.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "Pending":
        raise HTTPException(status_code=400, detail="Order already paid or processed")

    # Simulate payment success
    reference = f"PAY-{randint(100000, 999999)}"

    payment = Payment(
        order_id=order.id,
        reference=reference,
        amount=order.total_amount,
        status="Paid"
    )

    db.add(payment)
    order.status = "Paid"
    db.commit()
    db.refresh(payment)

    return payment