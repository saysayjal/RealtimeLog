import os
import pika
import json
import random
import time
from datetime import datetime
from pika.exceptions import AMQPConnectionError

levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
messages = [
    "User 'admin' logged in successfully.",
    "File 'data.txt' uploaded to server.",
    "Error: Database connection timeout (retrying...).",
    "System backup completed.",
    "Warning: Disk usage exceeds 85% on /dev/sda1.",
    "New user registered with email 'john@example.com'.",
    "Security alert: 3 failed login attempts for user 'admin'.",
    "Scheduled task executed successfully.",
    "API request took 1243ms (slow response).",
    "System shutdown initiated by user 'admin'."
]

def connect_to_rabbitmq(host, max_retries=5, delay=5):
    for i in range(max_retries):
        try:
            return pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=host,
                    port=5672,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
        except AMQPConnectionError as e:
            if i == max_retries - 1:
                raise
            time.sleep(delay)
            continue

def produce_logs():
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    connection = connect_to_rabbitmq(rabbitmq_host)
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host,
            port=5672,  # explicit port
            heartbeat=600,
            blocked_connection_timeout=300
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='raw_logs', durable=True)
    
    while True:
        log = {
            "level": random.choice(levels),
            "message": random.choice(messages),
            "timestamp": datetime.now().isoformat(),
        }
        channel.basic_publish(
            exchange='',
            routing_key='raw_logs',
            body=json.dumps(log),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f"Produced: {log}")
        time.sleep(1)

if __name__ == "__main__":
    produce_logs()