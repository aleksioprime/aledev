FROM nginx:1.27.1-alpine3.20-slim

# Устанавливаем certbot и плагин для nginx через apk
RUN apk add --no-cache certbot certbot-nginx

RUN mkdir -p /usr/share/nginx/html/mysite \
    && mkdir -p /usr/share/nginx/html/blog \
    && mkdir -p /var/www/certbot

# COPY /mysite_dist /usr/share/nginx/html/mysite
# COPY /blog_dist /usr/share/nginx/html/blog

CMD ["nginx", "-g", "daemon off;"]