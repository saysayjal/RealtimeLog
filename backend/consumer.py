import os
import pika
import json
import aio_pika
import asyncio

from aio_pika.abc import AbstractChannel
from aio_pika.exceptions import AMQPConnectionError

async def connect_to_rabbitmq(max_retries=5, retry_delay=5):
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    rabbitmq_user = os.getenv('RABBITMQ_USER', 'guest')
    rabbitmq_pass = os.getenv('RABBITMQ_PASSWORD', 'guest')
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}: Connecting to RabbitMQ...")
            connection = await aio_pika.connect_robust(
                f"amqp://{rabbitmq_user}:{rabbitmq_pass}@{rabbitmq_host}/",
                timeout=30,
                client_properties={"connection_name": "critical_logs_consumer"}
            )
            print("Successfully connected to RabbitMQ")
            return connection
        except AMQPConnectionError as e:
            print(f"Connection failed: {str(e)}")
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(retry_delay)

async def filter_critical_logs():
    try:
        connection = await connect_to_rabbitmq()
        channel = await connection.channel()
        

        raw_logs_queue = await channel.declare_queue("raw_logs", durable=True)
        critical_logs_queue = await channel.declare_queue("critical_logs", durable=True)
        
        async with raw_logs_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    log_data = json.loads(message.body.decode())
      
                    if log_data["level"] in ["ERROR", "CRITICAL"]:
                        await channel.default_exchange.publish(
                            aio_pika.Message(
                                body=message.body,
                                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                            ),
                            routing_key="critical_logs"
                        )
          
    except Exception as e:
        print(f"Error in consumer: {str(e)}")
        raise
    finally:
        if 'connection' in locals():
            await connection.close()


if __name__ == "__main__":
    asyncio.run(filter_critical_logs())