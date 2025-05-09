from database import Base
from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey,CheckConstraint
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True)
    username=Column(String(25),unique=True)
    email=Column(String(80),unique=True)
    password=Column(Text,nullable=True)
    is_staff=Column(Boolean,default=False)
    is_active=Column(Boolean,default=False)
    orders=relationship('Order',back_populates='user')


    def __repr__(self):
        return f"<User {self.username}>"


class Order(Base):
    ORDER_STATUSES = ['PENDING', 'IN-TRANSIT', 'DELIVERED']
    PIZZA_SIZES = ['SMALL', 'MEDIUM', 'LARGE', 'EXTRA-LARGE']

    __tablename__='orders'
    id=Column(Integer,primary_key=True)
    quantity=Column(Integer,nullable=False)
    order_status=Column(String(20),default="PENDING")
    pizza_size=Column(String(20),default="SMALL")
    user_id=Column(Integer,ForeignKey('user.id'))
    user=relationship('User',back_populates='orders')

    __table_args__ = (
        CheckConstraint(
            order_status.in_(ORDER_STATUSES),
            name='valid_order_status'
        ),
        CheckConstraint(
            pizza_size.in_(PIZZA_SIZES),
            name='valid_pizza_size'
        ),
    )

    def __repr__(self):
        return f"<Order {self.id}>"