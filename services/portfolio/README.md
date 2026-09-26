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

### Обратная связь через Яндекс Почту

Письма с формы на сайте отправляются по SMTP через `smtp.yandex.ru:465` (SSL).

1. В настройках ящика Яндекса включите «Почтовые программы → С сервера imap.yandex.ru по протоколу IMAP»
   (без этого SMTP-авторизация не пройдёт): https://mail.yandex.ru/#setup/client
2. Создайте пароль приложения: https://id.yandex.ru/security/app-passwords → «Почта».
   Обычный пароль от аккаунта не подойдёт.
3. Заполните в `ENV_PORTFOLIO_VARS`:
```
SMTP_HOST=smtp.yandex.ru
SMTP_PORT=465
SMTP_USE_SSL=true
SMTP_USER=<логин>@yandex.ru
SMTP_PASSWORD=<пароль_приложения>
FEEDBACK_SENDER_NAME=AleDev
FEEDBACK_SENDER=            # пусто = SMTP_USER (Яндекс не даёт слать от чужого адреса)
FEEDBACK_RECEIVER=          # пусто = SMTP_USER
TURNSTILE_SECRET_KEY=<your_turnstile_secret_key>
```

Если почта домена `aledev.ru` подключена к Яндекс 360, можно использовать ящик вида `no-reply@aledev.ru`
в `SMTP_USER` — тогда письма будут уходить с адреса домена.

В письме выставляется `Reply-To` с адресом посетителя, поэтому на сообщение можно ответить прямо из почты.

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
## Справочные команды:

Удаление контейнеров и переменных:
```
docker compose -f ~/aledev/services/portfolio/docker-compose.prod.yaml down - v
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
