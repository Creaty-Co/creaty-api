FROM ghcr.io/creaty-co/creaty-web/web:latest as web

FROM nginx:1.23.3 as nginx

WORKDIR /etc/nginx

ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache

COPY ./certs /certs
COPY ./nginx.stage.conf.conf ./templates/nginx.conf.conf
COPY --from=web /web ./html
