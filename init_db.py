from database import engine, Base
from models import User, Orders

Base.metadata.create_all(bind=engine)