# 🧠 Tom's Coding Platform – Backend

This is the backend server for Tom's Coding Web App. It uses **FastAPI** and **MongoDB** to serve code block data and real-time collaboration via WebSockets.

---

## 📦 Tech Stack

- FastAPI (Python)
- MongoDB (via Docker)
- Motor (async MongoDB driver)
- Uvicorn (ASGI server)

---

## 🚀 Getting Started

###  Create and Activate a Virtual Environment
```bash
python -m venv backendVenv
# Activate on Windows
backendVenv\Scripts\activate
# Or on Mac/Linux
source backendVenv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Running MongoDB with Docker
```bash
docker run -d -p 27017:27017 --name mongo-db mongo
```

### Running FastAPI server
```bash
uvicorn main:app --reload
```

### 🛑 Useful Docker Commands
```bash
docker stop mongo-db     # Stop the Mongo container
docker start mongo-db    # Start it again
docker ps                # See running containers
```

### ✅ Notes
Make sure MongoDB is running before starting the FastAPI server.
This backend serves an API consumed by a React frontend (not included here).