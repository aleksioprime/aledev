# Сервис блога

## Запуск сервиса

Скачайте репозиторий:
```
git clone https://github.com/aleksioprime/aledev.git
cd aledev
```

Запустите сервис локально:
```
cd services/blog
docker-compose -p aledev-blog up -d --build
```

Создание миграциий:
```shell
docker exec -it aledev-blog-app alembic revision --autogenerate -m "init migration"
```

Применение миграции (при перезапуске сервиса делается автоматически):
```shell
docker exec -it aledev-blog-app alembic upgrade head
```

Проверить базы:
```
docker exec -it aledev-blog-postgres psql -U admin blog -c "\dt"
```

# Запуск на сервере:

## Подготовка сервера

Проверьте установку docker compose
```
docker compose version
```

## Переменные окружения

Переменные окружения берутся из репозитория.

Для сервиса создаётся переменная `ENV_BLOG_VARS`, куда записываются все переменные из `.env.example`

## Добавление бесплатного SSL-сертификата

В контейнер фронтенда добавлен CertBot, с помощью которого происходит регистрация сертификата

Проверьте установку:
```
docker exec -it aledev-frontend certbot --version
```

Запустите CertBot для получения сертификатов
```
docker exec -it aledev-frontend certbot --nginx -d blog.aledev.ru -d www.blog.aledev.ru
ls -l /etc/letsencrypt/live/blog.aledev.ru/
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
docker exec -it aledev-frontend rm -rf /etc/letsencrypt/renewal/blog.aledev.ru.conf
docker exec -it aledev-frontend rm -rf /etc/letsencrypt/live/blog.aledev.ru
docker exec -it aledev-frontend rm -rf /etc/letsencrypt/archive/blog.aledev.ru
```
## Справочные команды:

Удаление контейнеров и переменных:
```
docker compose -f ~/aledev/services/blog/docker-compose.prod.yaml down - v
docker image prune -a -f
```

Посмотреть все volume:
```
docker volume ls
```

Удалить выбранный volume:
```
docker volume rm <volume_name>
```