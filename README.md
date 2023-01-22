# instant-proxy

Simple docker container which creates a reverse proxy with automatic configuration and SSL cert creation.

It tries to create and sign certificates with certbot, if this is not successful it uses openssl with self-signed certificates.

# Usage
### Connect to a container
```shell
docker run -d -p 443:443 \
  --name=proxy1 \
  -e CONTAINER_ADDR=myapp:3000 \
  --network=container:myapp \
  ghcr.io/1nbuc/instant-proxy
```
Starts a proxy which listens on port 443 and forwards all requests to container myapp:3000.

### Connect to localhost
```shell
docker run -d -p 443:443 \
  --add-host host.docker.internal:host-gateway
  --name=proxy1 \
   -e CONTAINER_ADDR=host.docker.internal:3000 \
  ghcr.io/1nbuc/instant-proxy
```

### Custom Ports (default is 443 and 80 to get exposed)
```shell
docker run -d -p 443:443 -p 44300 -p 80:80 -p 8080 \
  --name=proxy1 \
  -e CONTAINER_ADDR=myapp:3000 \
  -e SSL_PORTS=443,44300 \
  -e PORTS=80,8080 \
  --network=container:myapp \
  ghcr.io/1nbuc/instant-proxy
```

### Or use the docker-compose file


## With certbot
This currently only supports one domain.
It will use openssl if certbot fails.
```shell
docker run -d -p 443:443 \
  --name=proxy1 \
  -e CONTAINER_ADDR=myapp:3000 \
  -e SERVERNAMES=example.com \
  --network=container:myapp \
  ghcr.io/1nbuc/instant-proxy
```
