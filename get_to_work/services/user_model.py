from sqlalchemy import Column, Integer, String
from services.database import base
from sqlalchemy.dialects.postgresql import ARRAY

class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True) 
    email = Column(String, unique=True, index=True)
    password = Column(String)
    leetcodeUser = Column(String, unique=True, index=True) 
    completedProblems = Column(ARRAY(String))
    # LeetCode password
    # link to leaderboard object somehow