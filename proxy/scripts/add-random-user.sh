#!/usr/bin/env bash

set -euo pipefail

users_file="${1:-proxy/config/users.list}"

mkdir -p "$(dirname "$users_file")"
touch "$users_file"

generate_login() {
  while true; do
    candidate="proxy$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 10)"
    if ! awk -F: -v user="$candidate" '$1 == user { found = 1 } END { exit found ? 0 : 1 }' "$users_file"; then
      printf '%s\n' "$candidate"
      return
    fi
  done
}

generate_password() {
  LC_ALL=C tr -dc 'A-Za-z0-9!@#%^*_+=-' </dev/urandom | head -c 24
  printf '\n'
}

login="$(generate_login)"
password="$(generate_password)"

printf '%s:CL:%s\n' "$login" "$password" >> "$users_file"
chmod 600 "$users_file"

cat <<EOF
User added to ${users_file}
login=${login}
password=${password}
EOF
