# TaskFlow

A full-stack task management app built with React + FastAPI + MongoDB.

## Features

- Create, update, and delete tasks with priority levels
- Filter tasks by status (Todo / In Progress / Done)
- JWT authentication with secure bcrypt password hashing
- Async MongoDB with Motor driver
- REST API with auto-generated OpenAPI docs
- Responsive UI with Tailwind CSS

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, Tailwind CSS, Axios |
| Backend | Python, FastAPI, Motor (async MongoDB) |
| Database | MongoDB |
| Auth | JWT (python-jose) |

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser. API docs at `http://localhost:8000/docs`.

## API Endpoints

```
POST   /auth/register   - Register new user
POST   /auth/login      - Login & get JWT token
GET    /tasks           - List all tasks (paginated)
POST   /tasks           - Create task
GET    /tasks/{id}      - Get single task
PUT    /tasks/{id}      - Update task
DELETE /tasks/{id}      - Delete task
```

## License

MIT
