from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import aio_pika
import json
from datetime import datetime

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def log_consumer(websocket: WebSocket, queue_name: str):
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name, durable=True)
    
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                log_data = json.loads(message.body.decode())
            
                response = {
                    "message": log_data.get("message", ""),
                    "level": log_data.get("level", "INFO"),
                    "timestamp": log_data.get("timestamp", datetime.now().isoformat())
                }
                await websocket.send_text(json.dumps(response))

@app.websocket("/ws-logs")  
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await log_consumer(websocket, "critical_logs")
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()