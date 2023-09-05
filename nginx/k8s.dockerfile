FROM ghcr.io/creaty-co/creaty-web/web:latest as web

FROM nginx:1.23.3 as nginx

WORKDIR /etc/nginx

COPY ./certs /certs
COPY ./nginx.k8s.conf ./templates/nginx.conf.template
COPY --from=web /web ./html
