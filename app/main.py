from typing import List, Optional
from random import randrange
from fastapi import FastAPI, HTTPException, status, Depends

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{post_id}", response_model=schemas.Post)
def get_post(post_id: int,  db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found")
    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int,  db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post.delete(synchronize_session=False)
    db.commit()
    return {"message": "successfully deleted"}


@app.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    for field, value in updated_post.model_dump().items():
        setattr(post, field, value)

    db.commit()

    return post_query.first()
