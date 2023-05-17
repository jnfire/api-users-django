# api-users-django
Basic user administration api developed in django

### Requirements
First copy the file .envExample to .env and set the environment variables.

## Automatic start

## Manual start
### Start docker containers
```
docker compose -f docker-compose.dev.yaml up
```

### Create superuser
```
docker compose -f docker-compose.dev.yaml exec -T django bash -c "python3 manage.py runscript make_superuser"
```

## Open django shell
```
docker compose -f docker-compose.dev.yaml exec django bash
```

## Run tests
```
docker compose -f docker-compose.dev.yaml exec django bash -c "pytest"
```
