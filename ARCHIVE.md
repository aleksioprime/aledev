# Архив инфраструктурных сервисов

Ветка `archive/infra` — снимок репозитория до выделения портфолио в `main`.
Здесь сохранены сторонние сервисы, которые больше не входят в основную ветку:

| Каталог / файл | Что это |
| --- | --- |
| `3xui/` | Панель 3x-ui (Xray) + workflow `3xui-deploy.yml` |
| `proxy/` | 3proxy (HTTP/SOCKS) + workflow `proxy-deploy.yml` |
| `tunnel/` | Reverse SSH-туннель до домашнего сервера + workflow `tunnel-deploy.yml` |
| `frontend/nginx/nginx.conf` | Полный конфиг nginx с поддоменами через туннель (gitlab, argocd, registry, portainer, hyperspectrus, skeducator, skolstream, hello), заглушкой `portal` и `/vless` |
| `frontend/nginx/html/portal-aledev.html` | Страница-заглушка для `portal.aledev.ru` |

Workflow'ы деплоя этих стеков скачивают файлы из этой ветки (`raw.githubusercontent.com/.../archive/infra/...`),
поэтому их можно запускать вручную (`workflow_dispatch`), выбрав ветку `archive/infra`.
