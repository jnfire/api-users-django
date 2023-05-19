# api-users-django
Basic user administration api developed in django

### Requirements
First copy the file .envExample to .env and set the environment variables.

## Automatic start
Start with makefile if you have make installed on your system

### Start docker containers
``` 
make start.build
```

### Create fake data
```
make loaddata
```

Note: See all options in the makefile with the command:
```
make
```

See on http://api.localhost/

## Manual start
### Start docker containers
```
docker compose -f docker-compose.dev.yaml up
```

### Create superuser
```
docker compose -f docker-compose.dev.yaml exec -T django bash -c "python3 manage.py runscript make_superuser"
```

### Create 10 users
```
docker compose -f docker-compose.dev.yaml exec -T django bash -c "python3 manage.py runscript make_users"
```


## Open admin panel
See on http://api.localhost/admin/

### Credentials
```
user: admin
password: admin
```

### API endpoints list
- http://api.localhost/api/v1/ping/ (GET)
- http://api.localhost/api/v1/account/create/ (POST)
- http://api.localhost/api/v1/account/login/ (POST)
- http://api.localhost/api/v1/account/logout/ (GET)
- http://api.localhost/api/v1/account/profile/ (GET/PUT)

Note: See de API documentation for more details.

## API Documentation
### [API docs (Spanish)](https://lilac-swordtail-1ab.notion.site/API-de-usuarios-f3ec1b392dff4ade97f25b9df035a5fa)
### Postman
Import file ***api-of-users.postman_collection.json*** to postman for use the api.


## Other commands

### Open django shell
```
docker compose -f docker-compose.dev.yaml exec django bash
```

### Run tests
```
docker compose -f docker-compose.dev.yaml exec django bash -c "pytest"
```
