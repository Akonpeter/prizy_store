from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.routes import auth

from app.api.routes import products



app = FastAPI(
    title="Prizy Store API",
    version="1.0.0"
)




# Create database table

Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(products.router)


@app.get("/")
def root():
    return {"message": "Welcome to Prizy Store."}