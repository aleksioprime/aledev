# 3proxy (separate stack)

`proxy/docker-compose.prod.yaml` запускает один контейнер `aledev-3proxy` в отдельном compose-стеке.

Основные сервисы (`docker-compose.prod.yaml`, frontend/auth/portfolio, tunnel) этим стеком не меняются.

Стек использует официальный docker-образ `3proxy/3proxy`, потому что он рассчитан на внешний `3proxy.cfg`. Вариант с `ghcr.io/tarampampam/3proxy` лучше подходит для конфигурации через env, а не для нашего файлового конфига.

## Нужен ли `3proxy.cfg`

Технически можно жить и без явного `3proxy.cfg`, если использовать docker-образ с генерацией конфига из env.

Для этого проекта явный `3proxy.cfg` лучше:
- понятнее ACL и правила доступа
- пользователи лежат в отдельном `users.list`
- проще деплоить и поддерживать на сервере

## Что поднимается

- HTTP proxy на порту `3128`
- SOCKS proxy на порту `1080`
- HTTP proxy через внешний parent на порту `35103`
- SOCKS proxy через внешний parent на порту `51111`
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
- `proxy/config/upstreams.cfg` - дополнительные локальные порты, отправляющие трафик через внешние proxy
- `proxy/config/upstreams.cfg.example` - шаблон upstream-конфига
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

## Дополнительные upstream-порты

Основной `proxy/config/3proxy.cfg` включает файл `proxy/config/upstreams.cfg`.

Это позволяет поднять дополнительные локальные порты на вашем VPS, которые будут отправлять трафик через внешний parent proxy. Клиенты при этом продолжают входить вашими локальными пользователями из `users.list`.

Сейчас настроено:
- локальный HTTP proxy на `35103` -> через внешний HTTP proxy `195.26.226.75:35103`
- локальный SOCKS proxy на `51111` -> через внешний SOCKS5 proxy `195.26.226.75:51111`

Важно:
- клиент подключается к вашему серверу и использует ваш локальный логин/пароль из `users.list`
- логин/пароль upstream-прокси используются только внутри `upstreams.cfg`
- если хотите ограничить доступ к этим портам отдельными локальными пользователями, это можно сделать через `allow user1,user2`

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
- скачивает `proxy/config/upstreams.cfg.example`
- записывает `~/aledev/proxy/config/users.list` из GitHub secret
- записывает `~/aledev/proxy/config/upstreams.cfg` из GitHub secret при наличии
- перезапускает отдельный proxy stack

## Required GitHub secret

- `PROXY_USERS_LIST` - содержимое файла `users.list`, например:

```text
user1:CL:very_strong_password
user2:CL:another_strong_password
```

- `PROXY_UPSTREAMS_CFG` - содержимое файла `upstreams.cfg`, если вы не хотите хранить upstream-настройки прямо на сервере вручную

Если secret пустой, workflow оставит существующий `~/aledev/proxy/config/users.list` на сервере как есть. Если файла на сервере ещё нет, деплой завершится ошибкой.

Для `PROXY_UPSTREAMS_CFG` логика мягче:
- если secret задан, он перезапишет `~/aledev/proxy/config/upstreams.cfg`
- если secret пустой, но файл уже существует на сервере, он будет переиспользован
- если secret пустой и файла ещё нет, будет создан шаблон из `upstreams.cfg.example`

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

Дополнительные порты:
- HTTP через внешний parent: порт `35103`
- SOCKS через внешний parent: порт `51111`

## Замечания по ресурсу сервера

Для вашего VPS это разумная стартовая конфигурация:
- `mem_limit: 128m`
- `cpus: 0.25`
- `maxconn 256` в `proxy/config/3proxy.cfg`

Если прокси будет использоваться не только вами или появятся долгие соединения, снижайте `maxconn` или увеличивайте RAM/добавляйте swap.


```sh
curl -v --proxy http://89.223.68.11:3128 --proxy-user 'proxypkdsjf42m6:NWanZy=tu!TB0FGVV89Icgq9' https://api.ipify.org
```

```sh
curl -v --proxy socks5h://89.223.68.11:1080 --proxy-user 'proxypkdsjf42m6:NWanZy=tu!TB0FGVV89Icgq9' https://api.ipify.org
```
