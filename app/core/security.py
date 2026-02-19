from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
# Auth Dependency
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import session
from app.core.database import SessionLocal
from app.models.user import User
from jose import JWTError

# Secret key (change in production)

SECRET_KEY ="supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str)  -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Create Auth Dependency

oauth2_scheme =OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close


def get_current_user(token: str = Depends(oauth2_scheme), db: session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")


        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=401, details="User not found")
    
    return user



def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"

        )
    return current_user
    
