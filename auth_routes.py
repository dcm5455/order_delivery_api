from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from  schemas import SignupModel
from models import User
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from werkzeug .security import generate_password_hash, check_password_hash
from fastapi import status
auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@auth_router.get('/')
async def hello_world():
    return {"message": "Hello World"}

session = Session(bind=engine)
@auth_router.post('/signup',response_model=SignupModel,status_code=status.HTTP_201_CREATED)
async def signup(uses:SignupModel):

    db_email = session.query(User).filter(User.email == uses.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_username = session.query(User).filter(User.username == uses.username).first()
    if db_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(
        username=uses.username,
        email=uses.email,
        password=generate_password_hash(uses.password),
        is_staff=uses.is_staff,
        is_active=uses.is_active
    )
    session.add(new_user)
    session.commit()
    return new_user