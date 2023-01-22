#!/bin/sh
mkdir /certs

# if certbot throws an error it will use OPENSSL
/app/certbot.sh || /app/create-certs.sh
python3 /app/create-config.py
nginx -g "daemon off;"
