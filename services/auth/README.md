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
docker exec -it aledev-auth-app alembic revision --autogenerate -m "init migration"
```

Применение миграции (при перезапуске сервиса делается автоматически):
```shell
docker exec -it aledev-auth-app alembic upgrade head
```

Создание суперпользователя:
```shell
docker-compose -p aledev-auth exec app python scripts/create_superuser.py \
  --username admin \
  --password Rp2lx3 \
  --email admin@aledev.ru
```