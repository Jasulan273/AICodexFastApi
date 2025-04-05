from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.chat import ChatHistory
from models.user import User
from database import get_db
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from routes.user import SECRET_KEY, ALGORITHM
import jwt
from datetime import datetime

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

class ChatHistoryResponse(BaseModel):
    id: int
    question: str
    answer: str
    timestamp: datetime

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).filter(User.email == payload["sub"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/ask", response_model=ChatResponse)
async def ask_question(
        request: ChatRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    try:
        from services.openai import get_tax_code_response
        answer = await get_tax_code_response(request.question)

        chat = ChatHistory(
            user_id=current_user.id,
            question=request.question,
            answer=answer
        )
        db.add(chat)
        db.commit()

        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=list[ChatHistoryResponse])
async def get_chat_history(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    try:

        history = db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id).all()
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))