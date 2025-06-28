import os
import time
import pymysql
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from infrastructure.database import Base, engine
from utils.db_utils import wait_for_db

from routes.auth import router as auth_router
from routes.admin import router as admin_router
from routes.dispenser import router as dispenser_router
from routes.notifications import router as notifications_router
from routes.accounts import router as accounts_router
from routes.users import router as users_router

def init_db():
    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup: conectando recursos...")
    wait_for_db()
    init_db()
    yield
    print("Shutdown: limpando recursos...")

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", summary="Hello World")
async def root():
    return {"message": "Hello World from ATM Backend!"}

@app.get("/health")
async def health_check():
    return {"status": "OK"}

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(dispenser_router)
app.include_router(notifications_router)
app.include_router(accounts_router)
app.include_router(users_router)
