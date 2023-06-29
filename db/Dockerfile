FROM postgres:15.3

COPY ./certs/crt.pem /ssl/server.crt
COPY ./certs/key.pem /ssl/server.key

COPY ./init-ssl.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/init-ssl.sh
