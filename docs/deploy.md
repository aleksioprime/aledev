# Деплой на сервер

Инструкция для развёртывания портфолио на новом (или пересобранном) сервере.
Адрес сервера и все настройки хранятся в **секретах GitHub** — в коде их нет, поэтому для переезда
на другой сервер достаточно обновить секреты и запустить workflow **Deploy**.

## Что где работает

| Компонент | Каталог на сервере | Контейнеры |
| --- | --- | --- |
| Системный nginx + certbot | `/etc/nginx/sites-available/aledev.ru` | — (порты 80, 443, SSL; рядом могут жить другие сайты) |
| Фронтенд (nginx со SPA, разводит поддомены по сервисам) | `~/aledev` | `aledev-frontend` (только `127.0.0.1:8080`) |
| Сервис авторизации | `~/aledev/services/auth` | `aledev-auth-app`, Postgres, Redis |
| Сервис портфолио | `~/aledev/services/portfolio` | `aledev-portfolio-app`, Postgres |
| Общие файлы (медиа) | `~/aledev/media` | монтируется во все сервисы |

`~` — домашний каталог пользователя из секрета `SERVER_USER`. Пути в compose-файлах относительные,
поэтому подойдёт как `root`, так и обычный пользователь с `sudo`.
Сервисы общаются через Docker-сеть `aledev-shared`.

Снаружи запросы принимает **системный nginx** сервера: он держит SSL и проксирует `aledev.ru`,
`auth.aledev.ru` и `portfolio.aledev.ru` в контейнер `aledev-frontend`. Так на одном сервере
могут работать и другие сайты. Порт контейнера меняется переменной `FRONTEND_PORT` в `ENV_VARS`
(по умолчанию `8080`).

## 1. Сервер

1. Ubuntu 22.04+ или другой поддерживаемый Linux.
2. Откройте в файрволе порты **80**, **443** и порт SSH.
3. Заранее установите Docker Engine и Docker Compose plugin, а также nginx и certbot:
   ```bash
   apt install nginx certbot python3-certbot-nginx
   ```
   Пользователь `SERVER_USER` должен иметь доступ к Docker daemon без `sudo` (обычно через группу `docker`),
   а если это не `root` — ещё и `sudo` без пароля для `nginx`, `systemctl`, `certbot`, `tee`, `cp`, `ln`.
4. Создайте SSH-ключ для GitHub Actions — на своём компьютере:
   ```bash
   ssh-keygen -t ed25519 -f aledev_deploy -N "" -C "github-actions@aledev"
   ssh-copy-id -i aledev_deploy.pub -p <SSH-порт> <пользователь>@<IP-сервера>
   ```
   Содержимое `aledev_deploy` (приватная часть) пойдёт в секрет `SSH_KEY`.

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

## 4. Деплой

В проекте один workflow — **Deploy** (`.github/workflows/deploy.yml`).

**Автоматически** — при пуше (слиянии PR) в `main`: собирается и деплоится только то, что изменилось.

| Изменились файлы | Что деплоится |
| --- | --- |
| `services/auth/**` | сервис авторизации |
| `services/portfolio/**` | сервис портфолио (перед сборкой прогоняются тесты — если упали, деплоя не будет) |
| `frontend/**`, `deploy/**`, `docker-compose.prod.yaml` | фронтенд + сайт в системном nginx и SSL |

Изменения только в документации (`*.md`) и в `.github/` деплой не запускают.

**Вручную** — **Actions → Deploy → Run workflow** (ветка `main`), например для первого деплоя
на новый сервер или после смены секретов:

| Параметр | Первый запуск | Обычное обновление |
| --- | --- | --- |
| Что деплоить | `all` | нужный сервис или `all` |
| Собрать образы | ✅ | ✅ (выключите, если образы в Docker Hub уже актуальны) |
| Перезаписать сайт в nginx | не нужно (при первом деплое он установится сам) | ✅ только если меняли `deploy/nginx/aledev.conf` |
| Email для Let's Encrypt | ваш email, если certbot на сервере ещё не настраивали | пусто |
| Домены | по умолчанию | по умолчанию |

Порядок шагов: тесты портфолио → сборка образов → auth → portfolio → фронтенд → сайт в системном nginx и SSL.
Миграции баз применяются автоматически при старте контейнеров.
Шаг SSL выпускает сертификат (или расширяет существующий на все домены), прописывает его в nginx
и включает редирект на HTTPS. Повторный запуск не перевыпускает действующий сертификат,
продлевает их системный `certbot.timer`.

> **Про конфиг сайта.** Certbot дописывает SSL-настройки прямо в `/etc/nginx/sites-available/aledev.ru`,
> поэтому при обычном деплое файл не перезаписывается. Он устанавливается при первом деплое (если там
> ещё чужой конфиг) или с флагом «Перезаписать сайт в nginx»; прежняя версия сохраняется в
> `~/aledev/deploy/backup/`, SSL certbot прописывает заново в том же запуске.
> Конфиг nginx внутри контейнера (`frontend/nginx/`) входит в образ и обновляется вместе с ним.

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
| `Setup SSH`: «Порт закрыт или не отвечает» / «SSH-сервер не отвечает раннеру» | с вашего компьютера порт открыт, а с GitHub — нет: файрвол, fail2ban (`fail2ban-client status sshd`) или хостер режет входящий SSH из-за рубежа. IP раннера выводится в логе шага |
| `Setup SSH`: «Сервер отклонил ключ» | публичная часть ключа не добавлена в `~/.ssh/authorized_keys` пользователя `SERVER_USER` |
| `Setup SSH`: «SSH_KEY не читается» / «не похож на приватный ключ» | в секрет попала публичная часть, ключ обрезан или с паролем — вставьте приватный ключ без passphrase целиком |
| `permission denied ... docker.sock` | добавьте `SERVER_USER` в группу `docker` и переподключитесь по SSH |
| Certbot: `DNS problem` / `Timeout during connect` | DNS ещё не обновился (нужны все домены из списка) или закрыт порт 80 |
| `address already in use` на `127.0.0.1:8080` | порт занят другой программой (`ss -tlnp \| grep 8080`) — задайте другой `FRONTEND_PORT` в `ENV_VARS` |
| В админке 401/403 на запросах к портфолио | разные `JWT_SECRET_KEY` в `ENV_AUTH_VARS` и `ENV_PORTFOLIO_VARS` |
| Письма не приходят | смотрите статус письма в админке → «Обращения» и `docker logs aledev-portfolio-app` |

## Полезные команды

```bash
docker compose -f ~/aledev/docker-compose.prod.yaml ps
docker compose -f ~/aledev/services/auth/docker-compose.prod.yaml logs -f
docker compose -f ~/aledev/services/portfolio/docker-compose.prod.yaml logs -f
nginx -t && systemctl reload nginx          # системный nginx
certbot certificates
docker exec aledev-frontend nginx -t        # nginx внутри контейнера
docker stats
```
