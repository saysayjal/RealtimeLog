# Real-Time Log Monitoring System
A real-time log monitoring system built using FastAPI, RabbitMQ, and WebSocket, designed to simulate high-frequency logs and stream only high-priority logs (ERROR and CRITICAL) to a live frontend.

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![RabbitMQ](https://img.shields.io/badge/rabbitmq-%23FF6600.svg?style=for-the-badge&logo=rabbitmq&logoColor=white)

# Features
- Simulates 10–20 logs/sec with random levels and messages
- Filters and streams only ERROR and CRITICAL logs in real-time
- WebSocket-based live updates on frontend

# Tech Stack
- Backend: FastAPI, RabbitMQ, Pika, WebSocket
- Frontend: HTML, React
- Containerization: Docker & Docker Compose

### Port Requirements
The following ports must be available:

| Port  | Service        | Protocol |
|-------|---------------|----------|
| 3000  | Frontend      | HTTP     |
| 8000  | Backend API   | HTTP/WS  |
| 5672  | RabbitMQ      | AMQP     |
| 15672 | RabbitMQ UI   | HTTP     |

# Setup Instructions
- git clone https://github.com/saysayjal/RealtimeLog
- cd Realtimelog
- docker-compose up --build


# TODOs (for Future Improvements)
- Add WebSocket authentication 
- Add reconnect logic for WebSocket in frontend
- Deploy to cloud
