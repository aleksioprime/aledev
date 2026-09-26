FROM node:22-alpine AS builder

# Устанавливаем рабочий каталог контейнера
WORKDIR /usr/src/app

# Позволяет запускать vite и другие инструменты напрямую
ENV PATH=/usr/src/app/node_modules/.bin:$PATH

# Внедряем все переменные окружения, которые нам понадобятся при сборке
ARG VITE_AUTH_URL
ARG VITE_PORTFOLIO_URL
ARG VITE_LOGGING
ARG VITE_TURNSTILE_SITE_KEY

ENV VITE_AUTH_URL=$VITE_AUTH_URL \
    VITE_PORTFOLIO_URL=$VITE_PORTFOLIO_URL \
    VITE_LOGGING=$VITE_LOGGING \
    VITE_TURNSTILE_SITE_KEY=$VITE_TURNSTILE_SITE_KEY

# Ставим зависимости строго по package-lock.json (воспроизводимая сборка)
COPY app/package.json app/package-lock.json ./
RUN npm ci --no-audit --no-fund

# Копируем все файлы фронтенда
COPY app ./

FROM builder AS dev
CMD ["npm", "run", "dev", "--", "--host"]

FROM builder AS prod-builder
RUN npm run build

FROM nginx:1.28-alpine AS prod

RUN apk add --no-cache certbot certbot-nginx \
    && mkdir -p /var/www/certbot

COPY --from=prod-builder /usr/src/app/dist /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx/snippets/ /etc/nginx/snippets/

CMD ["nginx", "-g", "daemon off;"]
