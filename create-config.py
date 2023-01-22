import os

SSL_PORTS = os.environ.get('SSL_PORTS')
PORTS = os.environ.get('PORTS')
SERVERNAMES = os.environ.get('SERVERNAMES')
CONTAINER_ADDR = os.environ.get('CONTAINER_ADDR')

if not CONTAINER_ADDR:
    raise ValueError('No container address provided')

SERVERNAMES = SERVERNAMES.replace(',', ' ') + ' localhost' if SERVERNAMES else 'localhost'

SSL_PORTS = SSL_PORTS.split(',') if SSL_PORTS else ["443"]
PORTS = PORTS.split(',') if PORTS else ["80"]

full_config = '''events {}
http { \n'''

for port in SSL_PORTS:
    CONFIG_STR = '''
    server {{
        listen {port} ssl http2;
        listen [::]:{port} ssl http2;
        server_name {servername};

        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src * data: 'unsafe-eval' 'unsafe-inline'" always;
        # add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

        ssl_certificate /certs/server.crt;
        ssl_certificate_key /certs/server.key;
        ssl_client_certificate /certs/server.crt;
        ssl_verify_client optional;

        location / {{
            proxy_pass http://{container_addr};
        }}
    }}
    '''.format(port=port, servername=SERVERNAMES, container_addr=CONTAINER_ADDR)
    full_config += CONFIG_STR

for port in PORTS:
    CONFIG_STR = '''
    server {{
        listen {port};
        listen [::]:{port};
        server_name {servername};

        location ~ /.well-known/acme-challenge {{
                allow all;
                root /var/www/html;
        }}

        location / {{
                rewrite ^ https://$host$request_uri? permanent;
        }}
    }}
    '''.format(port=port, servername=SERVERNAMES)
    full_config += CONFIG_STR

full_config += '}'

# check if /etc/nginx/default.conf exists
if not os.path.exists('/etc/nginx/default.conf'):

    with open('/etc/nginx/default.conf', 'w') as f:
        f.write(full_config)

print(full_config)
