from sqlalchemy import Column, Integer, String
from services.database import base

class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # omit?
    email = Column(String, unique=True, index=True)
    password = Column(String)
    # LeetCode username
    # LeetCode password
    # link to leaderboard object somehow