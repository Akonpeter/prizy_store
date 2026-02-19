from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.core.security import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



   

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise   HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": db_user.email, "role": db_user.role}

    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
        
    }

