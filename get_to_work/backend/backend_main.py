from fastapi import FastAPI, WebSocket, APIRouter
from leetcode_scraper import get_user_problems

gtw = FastAPI()
router = APIRouter()

@gtw.get("/")
async def root():
    return {"message": "test from app root"}

@router.get("/leetcode/progress")
def get_leetcode_progress():
    return get_user_problems()

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Connected to WebSocket")
    await websocket.close()