from fastapi import APIRouter, status, Depends, HTTPException
from database import engine
from sqlalchemy.orm import Session
from schemas import SignUpModel, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from auth_config import create_access_token, create_refresh_token, get_current_user
from  fastapi_jwt_auth import AuthJWT
auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

session = Session(bind=engine)

@auth_router.get('/')
async def hello(current_user: dict = Depends(get_current_user)):
    """
    ## Sample hello world route
    """
    return {"message": "Hello World"}

@auth_router.post('/signup',
    status_code=status.HTTP_201_CREATED
)
async def signup(user: SignUpModel):
    """
    ## Create a user
    This requires the following
    ```
            username:int
            email:str
            password:str
            is_staff:bool
            is_active:bool
    ```
    """
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the email already exists"
        )

    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the username already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)
    session.commit()

    return new_user

@auth_router.post('/login', status_code=200)
async def login(user: LoginModel):
    """     
    ## Login a user
    This requires
        ```
            username:str
            password:str
        ```
    and returns a token pair `access` and `refresh`
    """
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = create_access_token(data={"sub": db_user.username})
        refresh_token = create_refresh_token(data={"sub": db_user.username})

        response = {
            "access": access_token,
            "refresh": refresh_token
        }

        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid Username Or Password"
    )

#refreshing tokens

@auth_router.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
    """
    ## Create a fresh token
    This creates a fresh token. It requires an refresh token.
    """


    try:
        Authorize.jwt_refresh_token_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please provide a valid refresh token"
        ) 

    current_user=Authorize.get_jwt_subject()

    
    access_token=Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access":access_token})

