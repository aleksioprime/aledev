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

Проверить базы:
```
docker exec -it aledev-auth-postgres psql -U admin aledev -c "\dt"
```

Создание суперпользователя:
```shell
docker-compose -p aledev-auth exec app python scripts/create_superuser.py \
  --username admin \
  --password Rp2lx3 \
  --email admin@aledev.ru
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

## Добавление бесплатного SSL-сертификата

В контейнер фронтенда добавлен CertBot, с помощью которого происходит регистрация сертификата

Проверьте установку:
```
docker exec -it aledev-frontend certbot --version
```

Запустите CertBot для получения сертификатов
```
docker exec -it aledev-frontend certbot --nginx -d auth.aledev.ru -d www.auth.aledev.ru
ls -l /etc/letsencrypt/live/auth.aledev.ru/
```

Добавьте автообновление сертификатов (каждые 90 дней). Для этого откройте crontab:
```
sudo crontab -e
```

Добавьте строку:
```
0 3 * * * docker exec aledev-frontend certbot renew --quiet && docker exec aledev-frontend nginx -s reload
```

В случае необхожимости можно удалить сертификаты:
```
docker exec -it aledev-frontend rm -rf /etc/letsencrypt/renewal/auth.aledev.ru.conf
docker exec -it aledev-frontend rm -rf /etc/letsencrypt/live/auth.aledev.ru
docker exec -it aledev-frontend rm -rf /etc/letsencrypt/archive/auth.aledev.ru
```