from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)

@order_router.get('/')
async def hello_world():
    return {"message": "Hello World"}

