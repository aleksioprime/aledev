FROM nginx:1.27.1-alpine3.20-slim


RUN apk add --no-cache certbot certbot-nginx

RUN mkdir -p /usr/share/nginx/html/mysite \
    && mkdir -p /var/www/certbot

CMD ["nginx", "-g", "daemon off;"]