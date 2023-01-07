ARG TAG

FROM ghcr.io/creaty-co/creaty-web/web:$TAG as web

FROM nginx:1.23.3 as nginx

WORKDIR /etc/nginx

COPY ./certs /certs
COPY ./nginx.prod.conf.conf ./templates/nginx.conf.conf
COPY --from=web /web ./html
