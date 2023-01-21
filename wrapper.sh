#!/bin/sh
mkdir /certs
/app/create-certs.sh
python3 /app/create-config.py
nginx -g "daemon off;"
