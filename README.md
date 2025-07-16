# Домашний проект

## Запуск для разработчика

Скачайте репозиторий:
```
git clone https://github.com/aleksioprime/aledev.git
cd hyperspectrus
```

Запустите сервис локально:
```
docker-compose -p aledev up -d --build
```

# Запуск на сервере:

## Подготовка сервера

Установите сервер с ОС Ubuntu 22.04+

Выполните обновление пакетов:
```
sudo apt update && sudo apt upgrade -y
```

Установите Docker:
```
sudo apt update && sudo apt install -y docker.io
```

Установите Compose-плагин:
```
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```

Проверьте установку
```
docker compose version
```

## Переменные окружения

Переменные окружения берутся из репозитория.

Для загрузки контейнеров в Docker Hub используется:
```
DOCKER_HUB_USERNAME=<логин пользователя Docker Hub>
DOCKER_HUB_ACCESS_TOKEN=<access-токен, который был выдан в DockerHub>
```

Для деплоя приложения из репозитория на сервер используется:
```
SERVER_HOST=<IP-адрес сервера>
SERVER_SSH_KEY=<Приватный ключ для подключения к серверу по SSH>
SERVER_USER=<Имя пользователя сервера>
```

Для сервиса создаётся переменная `ENV_VARS`, куда записываются все переменные из `.env.example`

## Добавление бесплатного SSL-сертификата

В контейнер фронтенда добавлен CertBot, с помощью которого происходит регистрация сертификата

Проверьте установку:
```
docker exec -it aledev-frontend certbot --version
```

Запустите CertBot для получения сертификатов
```
docker exec -it aledev-frontend certbot --nginx -d aledev.ru -d www.aledev.ru
ls -l /etc/letsencrypt/live/aledev.ru/
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
docker exec -it aledev-frontend rm -rf /etc/letsencrypt/renewal/hyperspectrus.ru.conf
docker exec -it aledev-frontend rm -rf /etc/letsencrypt/live/hyperspectrus.ru
docker exec -it aledev-frontend rm -rf /etc/letsencrypt/archive/hyperspectrus.ru
```

Проверьте логи на сервере

```
docker compose -p aledev logs
docker logs aledev-frontend

docker compose -f ~/aledev/docker-compose.prod.yaml ps

docker compose -f ~/aledev/services/auth/docker-compose.prod.yaml ps

docker compose -f ~/aledev/services/hyperspectrus/docker-compose.aledev.yaml ps
```

Редактирование NGINX:
```
sudo nano ~/aledev/nginx/nginx.conf
docker exec -it aledev-frontend nginx -s reload
```

Проверить нагрузку:
```
docker stats
```

Формирование ключа:

```
python3 -c "import secrets; print(''.join(secrets.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_') for _ in range(86)))"
```

```
docker exec -it aledev-frontend certbot --nginx -d hyperspectrus.aledev.ru -d www.hyperspectrus.aledev.ru
```