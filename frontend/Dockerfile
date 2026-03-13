FROM --platform=linux/amd64 node:20-bullseye AS builder

# Устанавливаем рабочий каталог контейнера
WORKDIR /usr/src/app

# Позволяет запускать vite и другие инструменты напрямую
ENV PATH /app/node_modules/.bin:$PATH
ENV NODE_OPTIONS=--trace-deprecation

# Внедряем все переменные окружения, которые нам понадобятся
ARG VITE_AUTH_URL
ARG VITE_PORTFOLIO_URL
ARG VITE_LOGGING
ARG VITE_TURNSTILE_SITE_KEY

# Предоставлем переменную готовому контейнеру
ENV VITE_AUTH_URL=$VITE_AUTH_URL
ENV VITE_PORTFOLIO_URL=$VITE_PORTFOLIO_URL
ENV VITE_LOGGING=$VITE_LOGGING
ENV VITE_TURNSTILE_SITE_KEY=$VITE_TURNSTILE_SITE_KEY

# Копируем файлы пакетов в контейнер и устанавливаем их
COPY app/package.json ./
RUN npm install

# Копируем все файлы фронтенда
COPY app ./

FROM builder AS dev
CMD ["npm", "run", "dev", "--", "--host"]

FROM builder AS prod-builder
RUN npm run build

FROM nginx:1.27.1-alpine3.20-slim AS prod

RUN apk add --no-cache certbot certbot-nginx

RUN mkdir -p /var/www/certbot

COPY --from=prod-builder /usr/src/app/dist /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx/snippets/ /etc/nginx/snippets/

CMD ["nginx", "-g", "daemon off;"]
