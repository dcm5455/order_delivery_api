from database import Base
from sqlalchemy import create_engine    
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy_utils.types import ChoiceType

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    orders = relationship('Orders', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', created_at='{self.created_at}', is_staff={self.is_staff}, is_active={self.is_active})>"


class  Orders(Base):
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    )

    PIZZA_SIZES = (
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('extra_large', 'Extra Large')
    )
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    order_status= Column(ChoiceType(choices=ORDER_STATUS), nullable=False, default='pending')
    pizza_size= Column(ChoiceType(choices=PIZZA_SIZES), nullable=False, default='small')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='orders')
    user = relationship('User', back_populates='orders')



    def __repr__(self):
        return f"<Order(id={self.id}, name='{self.name}', created_at='{self.created_at}', order_status='{self.order_status}', user_id={self.user_id})>"