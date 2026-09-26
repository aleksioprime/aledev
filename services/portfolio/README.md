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

### Обратная связь

Форма на сайте принимает два типа обращений: **заказ** (тип работ, бюджет, сроки) и **вопрос**.

Как это работает:
1. `POST /api/v1/feedback/` проверяет капчу Turnstile и сразу сохраняет обращение в БД
   (таблица `feedback_messages`) — оно не потеряется, даже если почта недоступна.
2. Письмо отправляется фоновой задачей после ответа клиенту: сначала через SMTP Яндекса,
   при ошибке — через Resend (если задан `RESEND_API_KEY`).
3. Воркер в процессе приложения раз в `EMAIL_RETRY_INTERVAL_SECONDS` досылает неотправленные письма
   (до `EMAIL_MAX_ATTEMPTS` попыток с растущей паузой).
4. В админке (`/admin/feedback`) видны все обращения: фильтры, поиск, статус обработки, заметки,
   статус доставки письма и кнопка повторной отправки.

Настройка Яндекс Почты:
1. В настройках ящика включите «Почтовые программы → С сервера imap.yandex.ru по протоколу IMAP»
   (без этого SMTP-авторизация не пройдёт): https://mail.yandex.ru/#setup/client
2. Создайте пароль приложения: https://id.yandex.ru/security/app-passwords → «Почта».
3. Добавьте в `ENV_PORTFOLIO_VARS`:
```
SMTP_USER=alesemochkin@yandex.ru
SMTP_PASSWORD=<пароль_приложения>
FEEDBACK_RECEIVER=alesemochkin@yandex.ru
TURNSTILE_SECRET_KEY=<your_turnstile_secret_key>
# запасной канал (необязательно)
RESEND_API_KEY=<your_resend_api_key>
RESEND_SENDER=no-reply@aledev.ru
```

В письме выставляется `Reply-To` с адресом посетителя — ответить можно прямо из почты.

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
