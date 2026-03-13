# Reverse SSH Tunnels (separate stack)

`tunnel/docker-compose.prod.yaml` starts one container `aledev-tunnel-gw` in a separate compose stack.

Main services (`docker-compose.prod.yaml`, frontend/auth/portfolio) are not changed by this stack.

## Required GitHub secret

- `TUNNEL_HOME_PUBLIC_KEY` - public key from home server (one line from `~/.ssh/aledev_home.pub`).

`tunnel-deploy` writes this key to `~/aledev/tunnel/keys/home_server.pub`.

## Home server autossh command

Use the VPS SSH tunnel gateway port `2223`.

Important: keep `-R 0.0.0.0:...` because this stack publishes container ports to host ports and your current frontend nginx proxies to those host ports.

```bash
autossh -f -M 0 -N \
  -o "ServerAliveInterval=60" \
  -o "ServerAliveCountMax=3" \
  -o "ExitOnForwardFailure=yes" \
  -i ~/.ssh/aledev \
  -R 0.0.0.0:9005:localhost:9000 \
  -R 0.0.0.0:9011:localhost:8011 \
  -R 0.0.0.0:9021:localhost:8021 \
  -R 0.0.0.0:9088:localhost:8888 \
  -R 0.0.0.0:9050:localhost:5000 \
  -R 0.0.0.0:9058:localhost:5080 \
  -R 0.0.0.0:9080:localhost:30865 \
  tunnel@89.223.68.11 -p 46222
```

## Deploy

Run GitHub workflow `tunnel-deploy`.
