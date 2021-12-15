# dex-ea
 External adapter to cast mid price for DEX pools

## Create and change directory
```
mkdir dex-ea && cd dex-ea
```

## Create following files

### docker_compose.yml
```
version: "3.9"
services:
  adapter:
    image: gcr.io/tracer-external-adapters/dex
    platform: linux/amd64
    ports:
      - "8080:8080"
    environment:
      - ETH_HTTP_URL=${ETH_HTTP_URL}
      - NAME=${NAME}
      - DISCORD_WEBHOOK=${DISCORD_WEBHOOK}
    restart: always
```

### .env
```
ETH_HTTP_URL=${ETH_HTTP_URL}
NAME=${NAME}
DISCORD_WEBHOOK=${DISCORD_WEBHOOK}
```

## Run
```
docker-compose up
```