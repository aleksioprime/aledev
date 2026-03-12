# Blog App

Отдельное приложение блога в монорепозитории.

Структура:

- `frontend/` — frontend блога (Vue + Vite + Vuetify).
- `backend/` — backend блога (FastAPI + PostgreSQL).
- `docker-compose.yaml` — локальный запуск frontend + backend + db.
- `docker-compose.prod.yaml` — production-вариант.

## Локальный запуск

```bash
cd blog
docker compose up -d --build
```

Frontend: `http://localhost:8086`  
Backend API: `http://localhost:8503/api`

## Запуск backend отдельно

```bash
cd blog/backend
docker compose up -d --build
```
