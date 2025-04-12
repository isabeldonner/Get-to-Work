from fastapi import FastAPI, APIRouter, Depends, HTTPException
#from services import leetcode_scraper
from sqlalchemy.orm import Session
from services.database import engine, local, base
from services.user_model import User
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

gtw = FastAPI()
router = APIRouter()
gtw.include_router(router)

secretKey = 'B%-6#-Pr-(dhu99okj7F%tgH'
myAlgorithm = 'HS256'
expireMin = 30

#create a token to verify if a user is logged in, home can only be accessed if they have a token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(seconds=expireMin))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secretKey, algorithm=myAlgorithm)

gtw.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = local()
    try:
        yield db
    finally:
        db.close()

base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str 

@gtw.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this username already exists")
    new_user = User(username=user.username, password=user.password, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"User registered successfully!"}

@gtw.post("/login/")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.username)).first()
    if not existing_user:
        return {"message":"User does not exist!"}
    if existing_user.password != user.password:
        return {"message":"Incorrect password!"}
    access_token = create_access_token(data={"sub": existing_user.username})
    return {"message":"User logged in successfully!", "token": access_token}


#checking whats in the database
db = local()

users = db.query(User).all()

for user in users:
    print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Password: {user.password}")

db.close()

'''
user_sessions = {}
class SessionData(User):
    username: str
    leetcode_session: str
    token: str

@gtw.get("/")
async def root():
    return {"root_message": "Welcome to Get to Work!"}

@gtw.post("/store_cookies/{username}")
async def store_cookies(data: SessionData, username: str):
    """
    Chrome:
    1. F12/Inspect Element on leetcode.com (logged in)
    2. Go from the Elements tab to Application
    3. Scroll down to the Storage section, open the Cookies menu in storage
    4. In Cookies, select the option for https://leetcode.com
    5. Get the values for the cookies named LEETCODE_SESSION and csrftoken
    """
    user_sessions[username] = {"session": data.leetcode_session, "csrf": data.token}
    return {"message": "Cookies stored successfully!"}

@router.get("/leetcode/progress/{username}")
async def get_leetcode_progress(username: str):
    if username not in user_sessions:
        raise HTTPException(status_code=404, detail="User does not have session")
    session_data = user_sessions[username]
    leetcode_session = session_data["leetcode_session"]
    token = session_data["token"]
    problems = leetcode_scraper.get_user_problems(leetcode_session, token)
    return {"problems": problems}

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Connected to WebSocket")
    await websocket.close()
'''