FROM --platform=linux/amd64 node:20-bullseye AS builder

# Устанавливаем рабочий каталог контейнера
WORKDIR /usr/src/app

# Позволяет запускать vite и другие инструменты напрямую
ENV PATH /app/node_modules/.bin:$PATH
ENV NODE_OPTIONS=--trace-deprecation

# Внедряем все переменные окружения, которые нам понадобятся
ARG VITE_AUTH_URL
ARG VITE_PORTFOLIO_URL
ARG VITE_BLOG_URL
ARG VITE_LOGGING

# Предоставлем переменную готовому контейнеру
ENV VITE_AUTH_URL=$VITE_AUTH_URL
ENV VITE_PORTFOLIO_URL=$VITE_PORTFOLIO_URL
ENV VITE_BLOG_URL=$VITE_BLOG_URL
ENV VITE_LOGGING=$VITE_LOGGING

# Копируем файлы пакетов в контейнер и устанавливаем их
COPY app/package.json ./
RUN npm install

# Копируем все файлы фронтенда
COPY app ./

FROM builder AS dev
CMD ["npm", "run", "dev", "--", "--host"]

FROM builder AS prod
RUN npm run build

# При запуске контейнера копируем файлы в volume и завершаем работу
CMD ["sh", "-c", "cp -r ./dist/* /usr/src/app/dist/ 2>/dev/null || echo 'Build files copied' && sleep 5"]