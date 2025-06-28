import os
import time
import pymysql
from sqlalchemy.orm import Session
from infrastructure.database import SessionLocal
from infrastructure.bank_database import BankDatabase

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_bank_db(db: Session = next(get_db())):
    return BankDatabase(db)
