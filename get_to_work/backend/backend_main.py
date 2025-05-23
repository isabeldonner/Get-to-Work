from fastapi import FastAPI, APIRouter, Depends, HTTPException
from services.leetcode_scraper import get_user_code, get_submission_statistics, get_submission_id
from sqlalchemy.orm import Session
from services.database import engine, local, base
from services.user_model import User
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from pydantic import Field, field_validator 
import re
import jwt
from datetime import datetime, timedelta

#initialize the main FastAPI app instance and router
gtw = FastAPI()
router = APIRouter()
gtw.include_router(router)

#define configuration variables for JWT creation and validation
secretKey = 'B%-6#-Pr-(dhu99okj7F%tgH'
myAlgorithm = 'HS256'
expireMin = 30

#username and password length validation
min_pass_length = 8
min_username_length = 4
max_pass_length = 30
max_username_length = 30

#create a token to verify if a user is logged in, home can only be accessed if they have a token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(seconds=expireMin))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secretKey, algorithm=myAlgorithm)

#configure CORS middleware to allow requests from any origin
gtw.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#dependency to get the database session for each request
def get_db():
    db = local()
    try:
        yield db
    finally:
        db.close()
#ensure that it's closed after the request is done

#initialize the database and create the tables if they don't exist
base.metadata.create_all(bind=engine)

#Pydantic model defining expected structure for user registraton
class UserCreate(BaseModel):
    username: str 
    password: str 
    email: EmailStr
    leetcodeUser: str

#Pydantic model defining expected structure for user login
class UserLogin(BaseModel):
    username: str
    password: str 

#Pydantic model defining expected structure for user update
class UserUpdate(BaseModel):
    username: str
    leetcodeSesh: str
    csrfToken: str

#Pydantic model defining expected structure for requesting user data
class UserData(BaseModel):
    username: str

#Pydantic model defining expected structure for requesting friends
class AddFriend(BaseModel):
    username: str
    friendUsername: str


# API endpoints to handle registration request
@gtw.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if len(user.username) < min_username_length or len(user.username) > max_username_length:
        raise HTTPException(status_code=400, detail="Username must be between 4 and 30 characters")
    if len(user.password) < min_pass_length or len(user.password) > max_pass_length:
        raise HTTPException(status_code=400, detail="Password must be between 8 and 30 characters")
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this username already exists")
    existing_leetcode_user = db.query(User).filter(User.leetcodeUser == user.leetcodeUser).first()
    if existing_leetcode_user:
        raise HTTPException(status_code=400, detail="User with this leetcode username already exists")
    new_user = User(username=user.username, password=user.password, email=user.email, leetcodeUser=user.leetcodeUser)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"User registered successfully!"}

# API endpoints to handle login request
@gtw.post("/login/")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.username)).first()
    if not existing_user:
        return {"message":"User does not exist!"}
    if existing_user.password != user.password:
        return {"message":"Incorrect password!"}
    access_token = create_access_token(data={"sub": existing_user.username})
    return {"message":"User logged in successfully!", "token": access_token}

# API endpoints to handle user update request
@gtw.post("/update/")
def update_user(user: UserUpdate, db: Session = Depends(get_db)):
    dbUser = db.query(User).filter(User.username == user.username).first()
    try:
        submissions = get_user_code(user.leetcodeSesh, user.csrfToken, user.username)
        dbUser.completedProblems = submissions
        
        for problem in submissions:
            print('ok')
            print(problem)
            problemID = get_submission_id(user.username, problem)
            url = f"https://leetcode.com/problems/{problem}/submissions/{problemID[problem]}"
            print(url)
            
            stat = get_submission_statistics(url, user.leetcodeSesh, user.csrfToken)
            print(stat)
            dbUser.userStats[problem] = stat
        
            
        db.commit()
    except Exception as e:
        return {"message":"Invalid session or csrf token!", "cookieUpdated": False}
    return {"message": "User updated successfully!", "cookieUpdated": True}

# API endpoints to handle user data request
@gtw.post("/home/")
def return_data(user: UserData, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user.username).first()
    return { "completedProblems": user.completedProblems, "friendRequests": user.friendRequests, "stats": user.userStats, "friends": user.friends }

# API endpoints to handle friend request
@gtw.post("/friendRequest/")
def addFriend(user: AddFriend, db: Session = Depends(get_db)):
    friend_user = db.query(User).filter((User.username == user.friendUsername) | (User.email == user.friendUsername)).first()
    if not friend_user:
        return {"message":"User does not exist!"}
    if user.username in friend_user.friendRequests:
        return {"message": "Friend request already sent!"}
    friend_user.friendRequests.append(user.username)
    db.commit()
    return {"message":"Friend request sent!"}

#checking whats in the database

db = local()

users = db.query(User).all()

for user in users:
    print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Password: {user.password}, LeetCode User: {user.leetcodeUser}, Completed Problems: {user.completedProblems}, Friend Requests: {user.friendRequests}, friends: {user.friends}, User Stats: {user.userStats}")

db.close()

"""
^ this code for printing the database threw some errors on certain servers when running the frontend.
I solved the issue by commenting it out
On my end, I was able to print the database simply by running:

psql -d get_to_work -U postgres 
^ in the virtual environment to connect to the database

then 

\d users

to print the "users" table
"""














