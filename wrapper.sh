mkdir /certs
./create-certs.sh
python3 create-config.py
nginx -g "daemon off;"
