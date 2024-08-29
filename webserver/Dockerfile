FROM nginx:1.26.0-alpine

RUN apk update && apk add --no-cache openssl

COPY app /app
COPY default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/ssl/private /etc/ssl/certs && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/nginx-selfsigned.key \
    -out /etc/ssl/certs/nginx-selfsigned.crt \
    -subj "/C=CA/ST=Quebec/L=Quebec/O=/OU=/CN=localhost"