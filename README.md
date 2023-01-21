# instant-proxy

Simple docker container which creates a reverse proxy with automatic configuration and SSL cert creation.

It tries to create and sign certificates with certbot, if this is not successful it uses openssl with self-signed certificates.
