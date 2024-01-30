from typing import List, Optional
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .utils import hash
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='socialmedia',
                                user='postgres', password='m902191835', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("connection was successful")
        break
    except Exception as error:
        print("connecting ...")
        print("Error: ", error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
