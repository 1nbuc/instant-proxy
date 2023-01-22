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

CERTPATH = '/certs/server.crt'
KEYPATH = '/certs/server.key'

if os.path.isdir('/etc/letsencrypt/live'):
    CERTPATH = '/etc/letsencrypt/live/{}/fullchain.pem'.format(SERVERNAMES)
    KEYPATH = '/etc/letsencrypt/live/{}/privkey.pem'.format(SERVERNAMES)

full_config = ''

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

        ssl_certificate {certpath};
        ssl_certificate_key {keypath};

        location / {{
            proxy_pass http://{container_addr};
        }}
    }}
    '''.format(port=port, servername=SERVERNAMES, container_addr=CONTAINER_ADDR, certpath=CERTPATH, keypath=KEYPATH)
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


# check if /etc/nginx/default.conf exists
if not os.path.exists('/etc/nginx/proxy.conf'):

    with open('/etc/nginx/conf.d/proxy.conf', 'w') as f:
        f.write(full_config)

# move /etc/nginx/default.conf to /etc/nginx/default.conf.bak
os.rename('/etc/nginx/conf.d/default.conf', '/etc/nginx/conf.d/default.conf.bak')

print(full_config)
