#!/usr/bin/env bash
# Загружает compose-файл и .env (из ENV_FILE) на сервер и перезапускает сервис.
# Использование: deploy-compose.sh <каталог от ~> <compose-файл>
set -euo pipefail

DIR=$1
COMPOSE=$2

ssh server "mkdir -p ~/$DIR ~/aledev/media"
scp "$COMPOSE" "server:$DIR/docker-compose.prod.yaml"
printf '%s\n' "$ENV_FILE" | ssh server "umask 077 && cat > ~/$DIR/.env"

ssh server bash -s <<SCRIPT
set -e
cd ~/$DIR
docker compose -f docker-compose.prod.yaml pull
docker compose -f docker-compose.prod.yaml up -d --remove-orphans
docker compose -f docker-compose.prod.yaml ps
docker image prune -f
SCRIPT
echo "✓ ~/$DIR обновлён"
