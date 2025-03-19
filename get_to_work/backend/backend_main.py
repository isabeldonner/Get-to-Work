from fastapi import FastAPI, WebSocket, APIRouter
from services import leetcode_scraper

gtw = FastAPI()
router = APIRouter()
gtw.include_router(router)

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