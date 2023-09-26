FROM ghcr.io/creaty-co/creaty-web/web:latest as web

FROM nginx:1.23.3 as nginx

WORKDIR /etc/nginx

COPY ./certs /certs
COPY ./nginx.k8s.conf ./templates/nginx.conf.template
COPY --from=web /web ./html

# docker build -t k8s-nginx:latest nginx -f nginx/k8s.dockerfile
# docker tag k8s-nginx:latest registry.digitalocean.com/creaty/k8s-nginx:latest
# docker push registry.digitalocean.com/creaty/k8s-nginx:latest
# kubectl rollout restart deployment/nginx-deployment
