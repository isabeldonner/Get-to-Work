from fastapi import FastAPI, WebSocket, APIRouter, Depends, HTTPException
#from services import leetcode_scraper
from sqlalchemy.orm import Session
from database import engine, local, base, metadata
from user_model import User
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

@gtw.get("/")
async def root():
    return {"message": "test from app root UPDATED"}

@router.get("/leetcode/progress")
async def get_leetcode_progress():
    problems = leetcode_scraper.get_user_problems()
    return {"problems": problems}

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Connected to WebSocket")
    await websocket.close()