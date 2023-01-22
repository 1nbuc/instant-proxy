#!/bin/sh

if [ -z "$SERVERNAMES" ]; then
    echo "No domain specified"
    exit 1
fi

if [ -z "$EMAIL" ]; then
    echo "No email specified"
    exit 1
fi

/usr/bin/certbot certonly --standalone --preferred-challenges http --agree-tos -m "$EMAIL" -d "$SERVERNAMES" -n -v

openssl rsa -outform der -in /etc/letsencrypt/live/"$SERVERNAMES"/privkey.pem -out /certs/server.key
openssl  pkcs12 -export -out /certs/server.pfx -inkey /certs/server.key -in /certs/server.crt -passout pass:
