#!/usr/bin/env bash
# Выполняется на сервере: ставит сайт aledev.ru в системный nginx и выпускает SSL.
# Переменные: UPDATE_NGINX (1 — перезаписать конфиг), EMAIL (необязательно), DOMAINS.
set -e
SUDO=""; [ "$(id -u)" = 0 ] || SUDO="sudo -n"
SITE=/etc/nginx/sites-available/aledev.ru
PORT=$(grep -E '^FRONTEND_PORT=' ~/aledev/.env | cut -d= -f2 | tr -d '[:space:]"')
PORT=${PORT:-8080}

# Устанавливаем свой конфиг, если на сервере ещё старый (не наш) или просят перезаписать
if [ "$UPDATE_NGINX" = "1" ] || ! $SUDO grep -q 'managed by aledev-deploy' "$SITE" 2>/dev/null; then
  if $SUDO test -f "$SITE"; then
    mkdir -p ~/aledev/deploy/backup
    $SUDO cp "$SITE" ~/aledev/deploy/backup/aledev.ru.$(date +%Y%m%d%H%M%S)
    echo "Старый конфиг сохранён в ~/aledev/deploy/backup/"
  fi
  sed "s/127.0.0.1:8080/127.0.0.1:$PORT/" ~/aledev/deploy/nginx-aledev.conf | $SUDO tee "$SITE" > /dev/null
  $SUDO ln -sf "$SITE" /etc/nginx/sites-enabled/aledev.ru
  echo "Конфиг сайта установлен"
else
  echo "Конфиг сайта уже наш — не перезаписываем"
fi
$SUDO nginx -t
$SUDO systemctl reload nginx

# Выпускает сертификат или расширяет существующий на новые домены и прописывает
# SSL в конфиг; действующий сертификат не перевыпускается. Продление — certbot.timer
ARGS=""
for d in $DOMAINS; do ARGS="$ARGS -d $d"; done
if [ -n "$EMAIL" ]; then ACCOUNT="--email $EMAIL"; else ACCOUNT="--register-unsafely-without-email"; fi
$SUDO certbot --nginx --non-interactive --agree-tos $ACCOUNT \
  --redirect --keep-until-expiring --expand $ARGS

# старое автообновление из контейнера больше не нужно
( crontab -l 2>/dev/null | grep -v 'aledev-certbot' ) | crontab - || true

curl -fsS -o /dev/null -H 'Host: aledev.ru' "http://127.0.0.1:$PORT/" && echo "Фронтенд отвечает"
echo "Готово!"
