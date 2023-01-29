FROM ghcr.io/creaty-co/creaty-web/web:latest as web

FROM nginx:1.23.3 as nginx

WORKDIR /etc/nginx

COPY ./nginx.dev.conf.conf ./templates/nginx.conf.conf
COPY --from=web /web ./html
