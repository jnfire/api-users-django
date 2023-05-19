DEFAULT_GOAL := help
help:
	@perl -nle'print $& if m{^[a-zA-Z_-|.]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

format: ## Format style with black
	black --exclude="/(postgres_data|venv|migrations|\.git)/" core/ apps/ scripts/ tests/

test: ## Tests
	docker compose -f docker-compose.dev.yaml exec -T django bash -c "pytest"

recreate: ## Recreate Django image
	docker compose -f docker-compose.dev.yaml build --no-cache --force-rm django
	docker compose -f docker-compose.dev.yaml up --force-recreate --no-deps -d django
	## make run.loaddata


loaddata: ## Load fake data
	# Remove database
	docker compose -f docker-compose.dev.yaml exec -T django bash -c "python3 manage.py flush --noinput"
	# Remove media
	sudo rm -rf static/*
	# Collect statics
	docker compose -f docker-compose.dev.yaml exec -T django bash -c "python3 manage.py collectstatic --noinput"
	# Remove media
	sudo rm -rf media/*
	# Add superuser: alias "admin" - password "admin"
	docker compose -f docker-compose.dev.yaml exec -T django bash -c "python3 manage.py runscript make_superuser"
	# Add default post categories
	docker compose -f docker-compose.dev.yaml exec -T django bash -c "python3 manage.py runscript make_users"

migrate: ## django makemigrations and migrate
	# Make migrations
	docker compose -f docker-compose.dev.yaml exec -T django bash -c "python3 manage.py makemigrations"
	# Migrate
	docker compose -f docker-compose.dev.yaml exec -T django bash -c "python3 manage.py migrate"

start.build: ## Start project
	# Create .env file from .envExample
	cp envExample .env
	# Start project
	docker compose -f docker-compose.dev.yaml up --build

start: ## Start project
	# Start project
	docker compose -f docker-compose.dev.yaml up

open: ## Open project to browser
	# Open project
	xdg-open http://api.localhost/