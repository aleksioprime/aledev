#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  echo "Usage: $0 <login> <password> [users_file]" >&2
  exit 1
fi

login="$1"
password="$2"
users_file="${3:-proxy/config/users.list}"

if ! printf '%s' "$login" | grep -Eq '^[A-Za-z0-9._-]+$'; then
  echo "Login must contain only letters, digits, '.', '_' or '-'" >&2
  exit 1
fi

case "$password" in
  *$'\n'*|*$'\r'*|"")
    echo "Password must not be empty or contain line breaks" >&2
    exit 1
    ;;
esac

mkdir -p "$(dirname "$users_file")"
touch "$users_file"

if awk -F: -v user="$login" '$1 == user { found = 1 } END { exit found ? 0 : 1 }' "$users_file"; then
  echo "User '${login}' already exists in ${users_file}" >&2
  exit 1
fi

printf '%s:CL:%s\n' "$login" "$password" >> "$users_file"
chmod 600 "$users_file"

echo "User '${login}' added to ${users_file}"
