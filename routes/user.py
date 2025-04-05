from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from database import get_db
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from typing import Optional

router = APIRouter()

# Настройки для JWT
SECRET_KEY = "taxcodexai"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")


    hashed_password = pwd_context.hash(user.password)
    new_user = User(email=user.email, password=hashed_password)


    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Пользователь успешно создан"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Проверка пользователя
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    # Генерация JWT-токена
    access_token = jwt.encode(
        {"sub": db_user.email, "exp": datetime.utcnow() + timedelta(minutes=1440)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": access_token, "token_type": "bearer"}