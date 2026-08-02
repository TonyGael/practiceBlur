from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from services import process_frame

router = APIRouter()

@router.get("/")
async def get_index():
    return FileResponse("static/index.html")

@router.websocket("/ws/video")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data_url = await websocket.receive_text()
            
            processed_url = process_frame(data_url)
            
            await websocket.send_text(processed_url)
    except WebSocketDisconnect:
        print("Cliente de WebSocket desconectado")
