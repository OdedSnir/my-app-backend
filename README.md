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
## important
python version neads to 3.11 and motor>=3.1


### Running FastAPI server
```bash
uvicorn main:app --reload
```
### ⚙️  Set Up the Backend on Ec2:
### 🛠️  EC2 Setup

- Launch an **Ubuntu EC2 instance**
- Allocate an **Elastic IP**
- Attach the Elastic IP to your instance
- Add **security group rules**:
  - Port `22` (SSH)
  - Port `80` (HTTP)
  - Port `8000` (backend)
  - Port `3000` (frontend)

---

### 🖥️ 2. SSH into your instance

```bash
ssh -i /path/to/your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

###🌐 3. Set Up the Frontend
Clone your frontend repo & enter the folder:


Clone your backend repo & enter the folder:
```bash
git clone https://github.com/OdedSnir/my-app-backend
cd your-backend-folder
```

Create and activate a virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate
```

💡 If Python 3.11 is not installed:

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv

```

Install dependencies:
```bash
pip install -r requirements.txt
```

Start the server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```


### 🚀  Run the backend persistently:
```bash
cd ~/backend/my-app-backend
source venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
```
### check if running:
```bash
ps aux | grep uvicorn
```
### kill Process
```bash
kill <pid>
```
### ✅ Notes
Make sure MongoDB is running before starting the FastAPI server.
This backend serves an API consumed by a React frontend (not included here).