# Деплой на сервер

Инструкция для развёртывания портфолио на новом (или пересобранном) сервере.
Адрес сервера и все настройки хранятся в **секретах GitHub** — в коде их нет, поэтому для переезда
на другой сервер достаточно обновить секреты и запустить workflow **Deploy All**.

## Что где работает

| Компонент | Каталог на сервере | Контейнеры |
| --- | --- | --- |
| Фронтенд + nginx + certbot | `~/aledev` | `aledev-frontend` (порты 80, 443) |
| Сервис авторизации | `~/aledev/services/auth` | `aledev-auth-app`, Postgres, Redis |
| Сервис портфолио | `~/aledev/services/portfolio` | `aledev-portfolio-app`, Postgres |
| Общие файлы (медиа) | `~/aledev/media` | монтируется во все сервисы |

`~` — домашний каталог пользователя из секрета `SERVER_USER`. Пути в compose-файлах относительные,
поэтому подойдёт как `root`, так и обычный пользователь с `sudo`.
Сервисы общаются через Docker-сеть `aledev-shared`.

## 1. Сервер

1. Ubuntu 22.04+ (подойдёт любой Linux, где работает `get.docker.com`).
2. Откройте в файрволе порты **80**, **443** и порт SSH.
3. Если деплоите не под `root`, пользователю нужен `sudo` без пароля
   (только для первой установки Docker; потом он попадает в группу `docker`).
4. Создайте SSH-ключ для GitHub Actions — на своём компьютере:
   ```bash
   ssh-keygen -t ed25519 -f aledev_deploy -N "" -C "github-actions@aledev"
   ssh-copy-id -i aledev_deploy.pub -p <SSH-порт> <пользователь>@<IP-сервера>
   ```
   Содержимое `aledev_deploy` (приватная часть) пойдёт в секрет `SSH_KEY`.

Docker вручную ставить не нужно — это сделает шаг **Prepare Server**.

## 2. DNS

A-записи на IP нового сервера:

```
aledev.ru            A  <IP>
www.aledev.ru        A  <IP>
auth.aledev.ru       A  <IP>
portfolio.aledev.ru  A  <IP>
```

Дождитесь, пока записи обновятся (`dig +short aledev.ru`), — без этого не выпустится SSL.

## 3. Секреты GitHub

**Settings → Secrets and variables → Actions → New repository secret**

| Секрет | Значение |
| --- | --- |
| `SERVER_HOST` | IP или домен сервера |
| `SERVER_USER` | пользователь SSH, например `root` |
| `SSH_PORT` | порт SSH, например `22` |
| `SSH_KEY` | приватный ключ целиком, вместе со строками `-----BEGIN/END ...-----` |
| `DOCKER_HUB_USERNAME` | логин Docker Hub |
| `DOCKER_HUB_ACCESS_TOKEN` | access-токен Docker Hub (Account settings → Personal access tokens) |
| `ENV_VARS` | переменные фронтенда, см. ниже |
| `ENV_AUTH_VARS` | заполненный `services/auth/.env.example` |
| `ENV_PORTFOLIO_VARS` | заполненный `services/portfolio/.env.example` |

`ENV_VARS` (фронтенд, подставляются при сборке образа):
```
VITE_AUTH_URL=https://auth.aledev.ru
VITE_PORTFOLIO_URL=https://portfolio.aledev.ru
VITE_TURNSTILE_SITE_KEY=<site key из Cloudflare Turnstile>
```

В `ENV_AUTH_VARS` и `ENV_PORTFOLIO_VARS` обратите внимание:
- `JWT_SECRET_KEY` должен **совпадать** в обоих сервисах — портфолио проверяет токены, выданные auth.
- Пароли баз данных придумайте новые (`POSTGRES_PASSWORD` = `DB_PASSWORD`).
- Для обратной связи в портфолио: `SMTP_USER`, `SMTP_PASSWORD` (пароль приложения Яндекса),
  `FEEDBACK_RECEIVER`, `TURNSTILE_SECRET_KEY`; запасной канал — `RESEND_API_KEY`.

Сгенерировать секретный ключ:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

## 4. Деплой одной кнопкой

**Actions → Deploy All → Run workflow** (ветка `main`):

| Параметр | Первый запуск | Обычное обновление |
| --- | --- | --- |
| Собрать образы | ✅ | ✅ |
| Подготовить сервер | ✅ | можно выключить |
| Перезаписать nginx.conf | не нужно (при первом деплое он загрузится сам) | ✅ только если меняли `frontend/nginx/nginx.conf` |
| Email для Let's Encrypt | ваш email | ваш email, если перезаписывали nginx.conf, иначе пусто |
| Домены | по умолчанию | по умолчанию |

Порядок шагов: подготовка сервера → сборка трёх образов → auth → portfolio → фронтенд → SSL.
Миграции баз применяются автоматически при старте контейнеров.
Шаг SSL выпускает сертификаты, прописывает их в nginx, включает редирект на HTTPS
и добавляет в `crontab` ежедневное автообновление. Повторный запуск не перевыпускает действующий сертификат.

Отдельные workflow (**Prepare Server**, **Build …**, **Deploy …**) по-прежнему можно запускать по одному.
Сборка образа также запускается автоматически при пуше в `main`, если менялся соответствующий сервис.

> **Про nginx.conf.** Certbot дописывает SSL-настройки прямо в `~/aledev/nginx/nginx.conf` на сервере,
> поэтому при обычном деплое файл не перезаписывается. Если включить «Перезаписать nginx.conf»,
> старая версия сохранится рядом как `nginx.conf.bak-<дата>`, а SSL надо вернуть — укажите email
> в том же запуске.

## 5. После первого деплоя

Создайте администратора (пароль придумайте свой):
```bash
cd ~/aledev/services/auth
docker compose -f docker-compose.prod.yaml exec app \
  python scripts/create_superuser.py --username admin --password '<пароль>' --email <email>
```

Войдите на `https://aledev.ru/admin` и добавьте проекты и опыт — на новом сервере базы пустые.

### Перенос данных со старого сервера (если он доступен)

```bash
# на старом сервере
docker exec aledev-portfolio-postgres pg_dump -U <DB_USER> <DB_NAME> > portfolio.sql
docker exec aledev-auth-postgres pg_dump -U <DB_USER> <DB_NAME> > auth.sql
tar czf media.tgz -C ~/aledev media

# на новом сервере (после первого деплоя)
docker exec -i aledev-portfolio-postgres psql -U <DB_USER> <DB_NAME> < portfolio.sql
docker exec -i aledev-auth-postgres psql -U <DB_USER> <DB_NAME> < auth.sql
tar xzf media.tgz -C ~/aledev
```
Имена контейнеров Postgres проверьте командой `docker ps`.

## 6. Проверка

```bash
docker ps                                   # все контейнеры в статусе Up
curl -I https://aledev.ru                   # 200
curl https://portfolio.aledev.ru/api/v1/ping/
nc -vz smtp.yandex.ru 465                   # открыт ли порт SMTP у хостера
docker logs aledev-portfolio-app --tail 50  # ошибки отправки писем видно здесь
```

Если хостер блокирует исходящий порт 465, письма уйдут через Resend (если задан `RESEND_API_KEY`),
а обращения в любом случае сохраняются и видны в админке → «Обращения».

## Частые проблемы

| Симптом | Причина / решение |
| --- | --- |
| `Setup SSH` падает на `ssh-keyscan` или `Permission denied` | неверные `SERVER_HOST` / `SSH_PORT` / `SSH_KEY`, или публичный ключ не добавлен в `~/.ssh/authorized_keys` |
| `sudo: a password is required` на Prepare Server | дайте пользователю `sudo` без пароля или деплойте под `root` |
| `permission denied ... docker.sock` | пользователь только что добавлен в группу `docker` — перезапустите workflow |
| Certbot: `DNS problem` / `Timeout during connect` | DNS ещё не обновился или закрыт порт 80 |
| В админке 401/403 на запросах к портфолио | разные `JWT_SECRET_KEY` в `ENV_AUTH_VARS` и `ENV_PORTFOLIO_VARS` |
| Письма не приходят | смотрите статус письма в админке → «Обращения» и `docker logs aledev-portfolio-app` |

## Полезные команды

```bash
docker compose -f ~/aledev/docker-compose.prod.yaml ps
docker compose -f ~/aledev/services/auth/docker-compose.prod.yaml logs -f
docker compose -f ~/aledev/services/portfolio/docker-compose.prod.yaml logs -f
docker exec aledev-frontend nginx -t && docker exec aledev-frontend nginx -s reload
docker exec aledev-frontend certbot certificates
docker stats
```
