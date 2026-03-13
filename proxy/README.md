# 3proxy (separate stack)

`proxy/docker-compose.prod.yaml` запускает один контейнер `aledev-3proxy` в отдельном compose-стеке.

Основные сервисы (`docker-compose.prod.yaml`, frontend/auth/portfolio, tunnel) этим стеком не меняются.

## Нужен ли `3proxy.cfg`

Технически можно жить и без явного `3proxy.cfg`, если использовать docker-образ с генерацией конфига из env.

Для этого проекта явный `3proxy.cfg` лучше:
- понятнее ACL и правила доступа
- пользователи лежат в отдельном `users.list`
- проще деплоить и поддерживать на сервере

## Что поднимается

- HTTP proxy на порту `3128`
- SOCKS proxy на порту `1080`
- аутентификация по логину/паролю для HTTP и SOCKS5

Ограничение протокола:
- SOCKS4/4.5 не поддерживает парольную аутентификацию так же, как SOCKS5
- если клиенту нужен логин/пароль, используйте SOCKS5

## Файлы

- `proxy/docker-compose.yaml` - локальный compose с относительными путями
- `proxy/config/3proxy.cfg` - основной конфиг сервера
- `proxy/docker-compose.prod.yaml` - серверный compose для деплоя на VPS
- `proxy/config/users.list` - список пользователей в формате `login:CL:password`
- `proxy/config/users.list.example` - шаблон файла пользователей
- `proxy/scripts/add-user.sh` - простой скрипт добавления пользователя

## Создание пользователей

Скопируйте пример:

```bash
cp proxy/config/users.list.example proxy/config/users.list
chmod 600 proxy/config/users.list
```

Добавить пользователя вручную:

```bash
echo 'myuser:CL:my_strong_password' >> proxy/config/users.list
chmod 600 proxy/config/users.list
```

Или через скрипт:

```bash
bash proxy/scripts/add-user.sh myuser my_strong_password
```

Сгенерировать случайного пользователя и пароль:

```bash
bash proxy/scripts/add-random-user.sh
```

Или в другой файл:

```bash
bash proxy/scripts/add-random-user.sh /root/aledev/proxy/config/users.list
```

Можно хранить несколько пользователей, по одному на строку:

```text
user1:CL:password1
user2:CL:password2
```

## Локальный запуск

```bash
cp proxy/config/users.list.example proxy/config/users.list
docker compose -f proxy/docker-compose.yaml up -d
docker logs --tail=50 aledev-3proxy
```

## Deploy

Есть отдельный GitHub workflow: `proxy-deploy`.

Он:
- создаёт `~/aledev/proxy`
- создаёт `~/aledev/proxy/config`
- скачивает `proxy/docker-compose.prod.yaml`
- скачивает `proxy/config/3proxy.cfg`
- записывает `~/aledev/proxy/config/users.list` из GitHub secret
- перезапускает отдельный proxy stack

## Required GitHub secret

- `PROXY_USERS_LIST` - содержимое файла `users.list`, например:

```text
user1:CL:very_strong_password
user2:CL:another_strong_password
```

Если secret пустой, workflow оставит существующий `~/aledev/proxy/config/users.list` на сервере как есть. Если файла на сервере ещё нет, деплой завершится ошибкой.

## Подключение клиентов

HTTP proxy:
- host: IP вашего сервера
- port: `3128`
- username/password: из `users.list`

SOCKS5:
- host: IP вашего сервера
- port: `1080`
- username/password: из `users.list`

SOCKS4/4.5:
- host: IP вашего сервера
- port: `1080`
- без гарантированной парольной аутентификации на уровне протокола

## Замечания по ресурсу сервера

Для вашего VPS это разумная стартовая конфигурация:
- `mem_limit: 128m`
- `cpus: 0.25`
- `maxconn 256` в `proxy/config/3proxy.cfg`

Если прокси будет использоваться не только вами или появятся долгие соединения, снижайте `maxconn` или увеличивайте RAM/добавляйте swap.
