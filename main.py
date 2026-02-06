from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

clients = []

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                await client.send_text(data)

    except WebSocketDisconnect:
        clients.remove(websocket)
        print("Client disconnected")

app.mount("/static", StaticFiles(directory="static"), name="static")
