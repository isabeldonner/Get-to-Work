from fastapi import FastAPI, WebSocket, APIRouter, Depends, HTTPException
from services import leetcode_scraper
from sqlalchemy.orm import Session
from database import engine, local, base, metadata
from services.user_model import User
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

gtw = FastAPI()
router = APIRouter()
gtw.include_router(router)

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
    email: str 

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
    return {"message":"user registered successfully"}

@gtw.post("/login/")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.username)).first()
    if not existing_user:
        return {"message":"no account"}
    if existing_user.password != user.password:
        return {"message":"incorrect password"}
    return {"message":"user logged in successfully"}

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