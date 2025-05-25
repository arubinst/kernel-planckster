## Build image

```bash
docker build --rm -t maany/kernel-planckster .
```

## Bring up the dependencies

```bash
docker compose -f docker-compose.yml --profile storage up -d
```

## Run the Docker container

I had to add two options to make it work. 

- One is to force the use of HTTP instead of HTTPS (we do not have certificates)

```bash
    -e KP_OBJECT_STORE_SECURE=false
```

- The other let's me connect to the kernel from any location (and not only localhost)
```bash
    -e KP_ALLOWED_ORIGINS="*" 
```

```bash
docker run -d --name kernel-planckster \
    -p 8000:8000 \
    -e KP_FASTAPI_HOST=0.0.0.0 \
    -e KP_FASTAPI_PORT=8000 \
    -e KP_RDBMS_HOST=db \
    -e KP_RDBMS_PORT=5432 \
    -e KP_RDBMS_USERNAME=postgres \
    -e KP_RDBMS_PASSWORD=postgres \
    -e KP_RDBMS_DBNAME=kp-db \
    -e KP_OBJECT_STORE_HOST=minio \
    -e KP_OBJECT_STORE_PORT=9000 \
    -e KP_OBJECT_STORE_ACCESS_KEY=minio \
    -e KP_OBJECT_STORE_SECRET_KEY=minio123 \
    -e KP_OBJECT_STORE_BUCKET=default \
    -e KP_OBJECT_STORE_SIGNED_URL_EXPIRY=60 \
    -e KP_OBJECT_STORE_SECURE=false \
    -e KP_ALLOWED_ORIGINS="*" \
    --network kernel-planckster_default \
    maany/kernel-planckster
```

## Logs

```bash
docker logs -f kernel-planckster
```

## Stop container

```bash
docker stop kernel-planckster && docker rm kernel-planckster
```

## Bring down the dependencies

```bash
docker compose -f docker-compose.yml --profile storage down
```
