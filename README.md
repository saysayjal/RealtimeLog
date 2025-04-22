# Real-Time Log Monitoring System
A real-time log monitoring system built using FastAPI, RabbitMQ, and WebSocket, designed to simulate high-frequency logs and stream only high-priority logs (ERROR and CRITICAL) to a live frontend.

# Features
- Simulates 10–20 logs/sec with random levels and messages
- Filters and streams only ERROR and CRITICAL logs in real-time
- WebSocket-based live updates on frontend

# Tech Stack
- Backend: FastAPI, RabbitMQ, Pika, WebSocket
- Frontend: HTML, React
- Containerization: Docker & Docker Compose

# Setup Instructions
- git clone https://github.com/saysayjal/RealtimeLog
cd Realtimelog
docker-compose up --build

# Folder Structure
Realtimelog/
│
├── backend/
│   ├── app/
│   ├── consumer.py
│   ├── main.py
│   ├── producer.py
│   ├── Dockerfile
│   ├── requirements.txt
│
├── frontedlog/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── Header/
│   │   │   └── LogCard/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│
├── docker-compose.yml
└── README.md

# TODOs (for Future Improvements)
- Add WebSocket authentication 
- Add reconnect logic for WebSocket in frontend
- Deploy to cloud
