from fastapi import HTTPException, status, Depends, APIRouter
from typing import List
from .. import models, schemas
from sqlalchemy.orm import Session
from ..utils import hash
from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserGet)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=List[schemas.UserGet])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{user_id}", response_model=schemas.UserGet)
def ger_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Post.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user
