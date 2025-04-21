import pika
import json
import random
import time
from datetime import datetime

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

def produce_logs():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
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