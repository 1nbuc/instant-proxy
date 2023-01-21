FROM nginx:1.21.3-alpine

# Install openssl
RUN apk add --no-cache openssl

# Install python3
RUN apk add --no-cache python3

WORKDIR /app

# Copy the script to create the config file
COPY create-config.py /app
COPY create-certs.sh /app
COPY wrapper.sh /app

RUN chmod +x create-certs.sh
RUN chmod +x wrapper.sh

CMD ["/app/wrapper.sh"]
