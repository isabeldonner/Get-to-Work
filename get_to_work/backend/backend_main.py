from fastapi import FastAPI, WebSocket

gtw = FastAPI()

@gtw.get("/")
async def root():
    return {"message": "test from app root"}

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Connected to WebSocket")
    await websocket.close()