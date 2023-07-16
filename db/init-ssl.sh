#!/bin/bash

set -e

cp /ssl/server.crt /var/lib/postgresql/data/
cp /ssl/server.key /var/lib/postgresql/data/
chown postgres:postgres /var/lib/postgresql/data/server.key
chown postgres:postgres /var/lib/postgresql/data/server.crt
chmod 600 /var/lib/postgresql/data/server.key

RUN echo "hostssl all all 0.0.0.0/0 md5" >>/var/lib/postgresql/data/pg_hba.conf
