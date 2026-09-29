# Сервис авторизации

## Запуск сервиса

Скачайте репозиторий:
```
git clone https://github.com/aleksioprime/aledev.git
cd aledev
```

Запустите сервис локально:
```
docker compose up -d --build auth-app
```

Если выходит ошибка `exec /usr/src/app/entrypoint.sh: permission denied`, то нужно вручную установить флаг выполнения для entrypoint.sh в локальной системе:
```
chmod +x app/entrypoint.sh
```

Создание миграциий:
```shell
docker exec -it aledev-auth-app alembic revision --autogenerate -m "init migration"
```

Применение миграции (при перезапуске сервиса делается автоматически):
```shell
docker exec -it aledev-auth-app alembic upgrade head
```

Проверить базы:
```
docker exec -it aledev-auth-postgres psql -U admin aledev -c "\dt"
```

Создание суперпользователя:
```shell
docker compose exec auth-app python scripts/create_superuser.py --username admin --password '<пароль>' --email <email>
```


# Запуск на сервере:

## Подготовка сервера

Проверьте установку docker compose
```
docker compose version
```

## Переменные окружения

Переменные окружения берутся из репозитория.

Для сервиса создаётся переменная `ENV_AUTH_VARS`, куда записываются все переменные из `.env.example`

## SSL-сертификат

SSL для всех доменов (включая этот сервис) выпускает certbot системного nginx сервера
во время деплоя фронтенда, продлевает — `certbot.timer`. Подробнее — [docs/deploy.md](../../docs/deploy.md).
