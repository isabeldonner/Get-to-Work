from sqlalchemy import Column, Integer, String
from backend.database import base

class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # omit?
    email = Column(String, unique=True, index=True)
    password = Column(String)