# 🧠 Wireframe Generator – Fullstack AI Application

An AI-powered fullstack web application that generates wireframes from natural language descriptions using Google's **Gemini 2.5 Flash** LLM and a multi-agent framework.

---

## 🔍 Overview

This tool allows users to describe what kind of UI they want (e.g., “Build a checkout page for a fashion e-commerce site”), and the system returns:
- A rendered wireframe (in the frontend)
- SVG code for the wireframe
- Additional planning and requirement insights

---

## 🛠 Tech Stack

### 🔗 Backend
- **FastAPI** (Python)
- **LangGraph** for multi-agent orchestration
- **LLM**: Google’s `gemini-2.5-flash-preview-04-17`
- **Docker** for containerization

### 🎨 Frontend
- **React**
- **TypeScript**
- **Material UI** (MUI)

---

## ✨ Features

- Natural language to wireframe generation
- Modular LLM agent architecture:
  - Requirements Gathering Agent
  - Planning Agent
  - SVG Generation Agent
- FastAPI docs at `/docs`
- Fully Dockerized backend
- Modern and responsive frontend with preview + SVG code

---

## 🧩 Folder Structure

Wireframe-FullStack/
│
├── wireframe-backend/
│ └── Wireframe-Generator/
│ ├── app/
│ ├── .env.example
│ ├── requirements.txt
│ ├── docker-compose.yml
│ └── Dockerfile
│
├── wireframe-frontend/
│ └── ... (React + MUI App)
│
└── README.md <-- You're here!



---

## 🚀 Getting Started

### ⚙️ Prerequisites

- Python 3.11+
- Node.js + npm
- Docker & Docker Compose *(optional for local run)*

---

### 🧪 Running Backend Locally

1. **Navigate to backend**:
```bash
cd wireframe-backend/Wireframe-Generator
```

2. **Setup environment**: 
cp .env.example .env
# Add your Google API key, etc. to `.env`

3. **Install dependencies**:

``` bash 
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)
pip install -r requirements.txt

```

4. **Run server**:
``` bash 
uvicorn app.main:app --reload
```


### 🌐 Running Frontend Locally
1. **Navigate to frontend**:

``` bash
cd wireframe-frontend
 ```

2. **Install dependencies**:
```bash
npm install 
```

4. **Start the dev server**:
``` bash
npm run dev
# or npm start
Visit http://localhost:3000
```


### 🐳 Docker Option
From the backend root (Wireframe-Generator):

``` bash
docker-compose up --build
```

### 🎨 Frontend Preview
1. Enter a query like:
"Design a responsive checkout page for a fashion e-commerce app"

2. See:
. Rendered wireframe

. SVG code in a separate tab

📄 License
MIT

