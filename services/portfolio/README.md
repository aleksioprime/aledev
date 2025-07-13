# Сервис портфолио

## Запуск сервиса

Скачайте репозиторий:
```
git clone https://github.com/aleksioprime/aledev.git
cd aledev
```

Запустите сервис локально:
```
cd services/portfolio
docker-compose -p aledev-portfolio up -d --build
```

Если выходит ошибка `exec /usr/src/app/entrypoint.sh: permission denied`, то нужно вручную установить флаг выполнения для entrypoint.sh в локальной системе:
```
chmod +x app/entrypoint.sh
```

Создание миграциий:
```shell
docker exec -it aledev-portfolio-app alembic revision --autogenerate -m "init migration"
```

Применение миграции (при перезапуске сервиса делается автоматически):
```shell
docker exec -it aledev-portfolio-app alembic upgrade head
```

Проверить базы:
```
docker exec -it aledev-portfolio-postgres psql -U admin portfolio -c "\dt"
```

# Запуск на сервере:

## Подготовка сервера

Проверьте установку docker compose
```
docker compose version
```

## Переменные окружения

Переменные окружения берутся из репозитория.

Для сервиса создаётся переменная `ENV_PORTFOLIO_VARS`, куда записываются все переменные из `.env.example`

## Добавление бесплатного SSL-сертификата

В контейнер фронтенда добавлен CertBot, с помощью которого происходит регистрация сертификата

Проверьте установку:
```
docker exec -it aledev-frontend certbot --version
```

Запустите CertBot для получения сертификатов
```
docker exec -it aledev-frontend certbot --nginx -d portfolio.aledev.ru -d www.portfolio.aledev.ru
ls -l /etc/letsencrypt/live/portfolio.aledev.ru/
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
docker exec -it aledev-frontend rm -rf /etc/letsencrypt/renewal/portfolio.aledev.ru.conf
docker exec -it aledev-frontend rm -rf /etc/letsencrypt/live/portfolio.aledev.ru
docker exec -it aledev-frontend rm -rf /etc/letsencrypt/archive/portfolio.aledev.ru
```