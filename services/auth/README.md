# Сервис авторизации

## Запуск сервиса

Скачайте репозиторий:
```
git clone https://github.com/aleksioprime/aledev.git
cd aledev
```

Запустите сервис локально:
```
cd services/auth
docker-compose -p aledev-auth up -d --build
```

Если выходит ошибка `exec /usr/src/app/entrypoint.sh: permission denied`, то нужно вручную установить флаг выполнения для entrypoint.sh в локальной системе:
```
chmod +x app/entrypoint.sh
```

Создание миграциий:
```shell
docker exec -it empolimer-backend alembic revision --autogenerate -m "init migration"
```

Применение миграции (при перезапуске сервиса делается автоматически):
```shell
docker exec -it empolimer-backend alembic upgrade head
```

Создание суперпользователя:
```shell
docker-compose -p empolimer exec backend python scripts/create_superuser.py \
  --username superuser \
  --password 1q2w3e \
  --email admin@empolimer.ru
```