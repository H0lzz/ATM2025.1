import os
import time
import pymysql
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from models import User
from database import Base, engine
from pydantic import BaseModel
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

def wait_for_db():
    if os.getenv('WAIT_FOR_DB', 'false').lower() == 'true':
        max_retries = 10
        for _ in range(max_retries):
            try:
                conn = pymysql.connect(
                    host=os.getenv('DB_HOST'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    database=os.getenv('DB_NAME')
                )
                conn.close()
                return
            except pymysql.Error:
                time.sleep(5)
        raise Exception("Could not connect to MySQL after multiple attempts")

@app.on_event("startup")
async def startup():
    wait_for_db()

class UserCreate(BaseModel):
    username: str
    email: str

@app.get("/", summary="Hello World")
async def root():
    return {"message": "Hello World from ATM Backend!"}

@app.get("/health")
async def health_check():
    return {"status": "OK"}

@app.get("/docs", include_in_schema=False)
def redirect_to_swagger():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

@app.on_event("startup")
def startup():
    init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user