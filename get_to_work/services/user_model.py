from sqlalchemy import Column, Integer, String, JSON
from services.database import base
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.ext.mutable import MutableDict

# defines user model for storing user information in the database

class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True) 
    email = Column(String, unique=True, index=True)
    password = Column(String)
    leetcodeUser = Column(String, unique=True, index=True) 
    completedProblems = Column(JSONB, default = dict)
    friendRequests = Column(ARRAY(String), default = list)
    friends = Column(ARRAY(String), default = list)
    userStats = Column(MutableDict.as_mutable(JSON), default = dict)
    # LeetCode password
    # link to leaderboard object somehow




