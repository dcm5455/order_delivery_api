from fastapi import APIRouter, Depends, status, HTTPException
from models import User, Order
from schemas import OrderModel, OrderStatusModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder
from auth_config import get_current_user

order_router = APIRouter(
    prefix="/orders",
    tags=['orders']
)

session = Session(bind=engine)

@order_router.get('/')
async def hello(current_user: dict = Depends(get_current_user)):
    """
    ## A sample hello world route
    This returns Hello world
    """
    return {"message": "Hello World"}

@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, current_user: dict = Depends(get_current_user)):
    """
    ## Placing an Order
    This requires the following
    - quantity : integer
    - pizza_size: str
    """
    user = session.query(User).filter(User.username == current_user.username).first()

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity
    )

    new_order.user = user

    session.add(new_order)
    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)

@order_router.get('/orders')
async def list_all_orders(current_user: dict = Depends(get_current_user)):
    """
    ## List all orders
    This lists all orders made. It can be accessed by superusers
    """
    user = session.query(User).filter(User.username == current_user.username).first()

    if user.is_staff:
        orders = session.query(Order).all()
        return jsonable_encoder(orders)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not a superuser"
    )

@order_router.get('/orders/{id}')
async def get_order_by_id(id: int, current_user: dict = Depends(get_current_user)):
    """
    ## Get an order by its ID
    This gets an order by its ID and is only accessed by a superuser
    """
    user = session.query(User).filter(User.username == current_user.username).first()

    if user.is_staff:
        order = session.query(Order).filter(Order.id == id).first()
        return jsonable_encoder(order)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not allowed to carry out request"
    )

@order_router.get('/user/orders')
async def get_user_orders(current_user: dict = Depends(get_current_user)):
    """
    ## Get a current user's orders
    This lists the orders made by the currently logged in users
    """
    user = session.query(User).filter(User.username == current_user.username).first()
    return jsonable_encoder(user.orders)

@order_router.get('/user/order/{id}/')
async def get_specific_order(id: int, current_user: dict = Depends(get_current_user)):
    """
    ## Get a specific order by the currently logged in user
    This returns an order by ID for the currently logged in user
    """
    user = session.query(User).filter(User.username == current_user.username).first()

    for order in user.orders:
        if order.id == id:
            return jsonable_encoder(order)
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No order with such id"
    )

@order_router.put('/order/update/{id}/')
async def update_order(id: int, order: OrderModel, current_user: dict = Depends(get_current_user)):
    """
    ## Updating an order
    This updates an order and requires the following fields
    - quantity : integer
    - pizza_size: str
    """
    order_to_update = session.query(Order).filter(Order.id == id).first()

    order_to_update.quantity = order.quantity
    order_to_update.pizza_size = order.pizza_size

    session.commit()

    response = {
        "id": order_to_update.id,
        "quantity": order_to_update.quantity,
        "pizza_size": order_to_update.pizza_size,
        "order_status": order_to_update.order_status,
    }

    return jsonable_encoder(response)

@order_router.patch('/order/update/{id}/')
async def update_order_status(
    id: int,
    order: OrderStatusModel,
    current_user: dict = Depends(get_current_user)
):
    """
    ## Update an order's status
    This is for updating an order's status and requires ` order_status ` in str format
    """
    user = session.query(User).filter(User.username == current_user.username).first()

    if user.is_staff:
        order_to_update = session.query(Order).filter(Order.id == id).first()
        order_to_update.order_status = order.order_status
        session.commit()

        response = {
            "id": order_to_update.id,
            "quantity": order_to_update.quantity,
            "pizza_size": order_to_update.pizza_size,
            "order_status": order_to_update.order_status,
        }

        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not allowed to carry out request"
    )

@order_router.delete('/order/delete/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_order(id: int, current_user: dict = Depends(get_current_user)):
    """
    ## Delete an Order
    This deletes an order by its ID
    """
    order_to_delete = session.query(Order).filter(Order.id == id).first()
    session.delete(order_to_delete)
    session.commit()
    return None