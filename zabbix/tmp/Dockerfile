FROM ghcr.io/creaty-co/creaty-web/web:latest as web

FROM nginx:1.23.3 as nginx

WORKDIR /etc/nginx

COPY ./nginx.conf ./conf.d/nginx.conf
COPY --from=web /web ./html
