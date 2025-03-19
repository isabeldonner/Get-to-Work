from fastapi import FastAPI, WebSocket, APIRouter, HTTPException
from services import leetcode_scraper, user_model

gtw = FastAPI()
router = APIRouter()
gtw.include_router(router)

user_sessions = {}
class SessionData(user_model.User):
    username: str
    leetcode_session: str
    token: str

@gtw.get("/")
async def root():
    return {"root_message": "Welcome to Get to Work!"}

@gtw.post("/store_cookies")
async def store_cookies(data: SessionData):
    """
    Chrome:
    1. F12/Inspect Element on leetcode.com
    2. Go from the Elements tab to Application
    3. Scroll down to the Storage section, open the Cookies menu in storage
    4. In Cookies, select the option for https://leetcode.com
    5. Get the values for the cookies named LEETCODE_SESSION and csrftoken
    """
    user_sessions[data.username] = {"session": data.leetcode_session, "csrf": data.token}
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