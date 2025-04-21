import pika
import json
import aio_pika
import asyncio

async def filter_critical_logs():
    # Setup RabbitMQ connection
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    
    # Declare queues
    raw_logs_queue = await channel.declare_queue("raw_logs", durable=True)
    critical_logs_queue = await channel.declare_queue("critical_logs", durable=True)
    
    async with raw_logs_queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                log_data = json.loads(message.body.decode())
                
                # Filter only ERROR and CRITICAL logs
                if log_data["level"] in ["ERROR", "CRITICAL"]:
                    await channel.default_exchange.publish(
                        aio_pika.Message(
                            body=message.body,
                            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                        ),
                        routing_key="critical_logs"
                    )
                    print(f"Forwarded critical log: {log_data}")

if __name__ == "__main__":
    asyncio.run(filter_critical_logs())