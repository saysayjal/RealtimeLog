import os
import asyncio
import aio_pika
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# Add CORS middleware to allow connections from your React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def log_consumer(websocket: WebSocket, queue_name: str):
    connection = None
    try:
        rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
        rabbitmq_port = int(os.getenv("RABBITMQ_PORT", "5672"))  # Convert to int
        rabbitmq_user = os.getenv("RABBITMQ_USER", "guest")
        rabbitmq_pass = os.getenv("RABBITMQ_PASSWORD", "guest")
        
        connection = await aio_pika.connect_robust(
            f"amqp://{rabbitmq_user}:{rabbitmq_pass}@{rabbitmq_host}:{rabbitmq_port}/",
            timeout=30  
        )

        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                try:
                    async with message.process():
                        log_data = json.loads(message.body.decode())
                        # Format the message to match your React component's expectations
                        response = {
                            "message": log_data.get("message", ""),
                            "level": log_data.get("level", "INFO"),
                            "timestamp": log_data.get("timestamp", datetime.now().isoformat())
                        }
                        await websocket.send_text(json.dumps(response))
                except json.JSONDecodeError:
                    print("Invalid message format")
                except Exception as e:
                    print(f"Error processing message: {e}")
                    break
    except aio_pika.exceptions.AMQPConnectionError as e:
        print(f"RabbitMQ connection error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if connection:
            await connection.close()

@app.websocket("/ws-logs")  # Changed to match your React client's URL
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:  
            try: 
                await log_consumer(websocket, "critical_logs")
            except WebSocketDisconnect:
                print("Client disconnected")
                break
            except Exception as e:
                print(f"Connection error, reconnecting: {e}")
                await asyncio.sleep(5)  # Wait before reconnecting
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        try:
            await websocket.close()
        except:
            pass