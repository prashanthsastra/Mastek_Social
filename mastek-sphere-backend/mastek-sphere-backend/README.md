# Mastek Sphere FastAPI Backend

Phase 1 backend for the Mastek Sphere hackathon MVP. It uses the existing PostgreSQL `mastek_sphere_dev` database and does **not** recreate the schema.

## Prerequisites
- Python 3.11+
- PostgreSQL running with `mastek_sphere_dev`
- The Phase 1 schema + seed data already loaded

## macOS / zsh setup
```bash
cd mastek-sphere-backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set your actual DB login. For local admin testing you may temporarily use your local PostgreSQL account, but the app should ultimately use `mastek_sphere_app`.

Example:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mastek_sphere_dev
DB_USER=mastek_sphere_app
DB_PASSWORD=YOUR_PASSWORD
CORS_ORIGINS=http://localhost:5173
```

Run:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open:
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/api/v1/health

## Main endpoints
- `GET /api/v1/health`
- `GET /api/v1/users?search=Azure`
- `GET /api/v1/users/{user_id}`
- `GET, POST /api/v1/posts`
- `POST, DELETE /api/v1/posts/{post_id}/like`
- `GET, POST /api/v1/posts/{post_id}/comments`
- `GET /api/v1/communities`
- `POST, DELETE /api/v1/communities/{id}/join`
- `GET /api/v1/guides?search=expense`
- `GET /api/v1/learning`
- `GET /api/v1/events`
- `GET /api/v1/radio/episodes`
- `GET /api/v1/culture-cast`
- `GET, POST /api/v1/recognition`
- `GET, POST /api/v1/saved`
- `GET /api/v1/notifications`
- `POST /api/v1/ai/chat` placeholder only

## Important
The `/demo/...` media URLs in seed data are placeholders. They require real frontend/static assets later.
