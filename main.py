from fastapi import APIRouter, Depends, HTTPException,FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from  auth_routes import auth_router
from order_routes import order_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, Request, Response

app = FastAPI()
app.include_router(auth_router)
app.include_router(order_router)