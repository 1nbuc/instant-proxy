openssl genrsa -out server.key 4096
touch openssl.cnf

cat >> openssl.cnf <<EOF
[ req ]
prompt = no
distinguished_name = req_distinguished_name

[ req_distinguished_name ]
C = GB
ST = Test State
L = Test Locality
O = Org Name
OU = Org Unit Name
CN = Common Name
emailAddress = test@email.com
EOF

openssl req -x509 -config openssl.cnf -nodes -days 7300 \
    -keyout /certs/server.key -out /certs/server.crt
