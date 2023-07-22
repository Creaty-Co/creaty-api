FROM ghcr.io/creaty-co/creaty-web/web:latest as web

RUN cp -r /web/ /http/ && \
    cp -r /web/ /https/ && \
    rm -r /web/ && \
    find /http/ -type f -exec sed -i \
        's|https://dev-api.creaty.club|http://api.local.host|g' {} + && \
    find /https/ -type f -exec sed -i \
        's|https://dev-api.creaty.club|https://api.local.host|g' {} + && \
    gzip -rkvf9 /http/ && \
    gzip -rkvf9 /https/

FROM nginx:1.23.3 as nginx

WORKDIR /etc/nginx/

RUN mkdir /certs/ && \
    openssl genpkey -algorithm RSA -out /certs/key.pem && \
    openssl req -new -x509 -key /certs/key.pem -out /certs/crt.pem -days 365 -subj \
        "/C=US/ST=State/L=City/O=Organization/OU=OrganizationalUnit/CN=*.local.host"
COPY ./certs/ /certs/

COPY ./nginx.local.conf.conf ./templates/nginx.conf.conf
COPY --from=web /http/ ./html/http/
COPY --from=web /https/ ./html/https/
