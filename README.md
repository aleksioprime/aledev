# aledev.ru — портфолио

Сайт-портфолио: фронтенд (Vue 3 + Vite), сервис портфолио (FastAPI) и сервис авторизации для админ-панели.

## Запуск для разработчика

Скачайте репозиторий:
```
git clone https://github.com/aleksioprime/aledev.git
cd aledev
```

Запустите сервис локально:
```
docker compose up -d --build
```

Корневой compose подключает dev-конфигурации auth и portfolio из каталогов сервисов.
Остановка всего стека: `docker compose down`.

# Деплой на сервер

Полная инструкция: [docs/deploy.md](docs/deploy.md).

Коротко:
1. Направить DNS (`aledev.ru`, `www`, `auth`, `portfolio`) на сервер и открыть порты 80/443.
2. Заполнить секреты GitHub: `SERVER_HOST`, `SERVER_USER`, `SSH_PORT`, `SSH_KEY`, `DOCKER_HUB_*`,
   `ENV_VARS`, `ENV_AUTH_VARS`, `ENV_PORTFOLIO_VARS`.
3. Запустить **Actions → Deploy All**: подготовка сервера (Docker), сборка образов, деплой
   auth → portfolio → фронтенд и, если указан email, выпуск SSL-сертификатов с автообновлением.
