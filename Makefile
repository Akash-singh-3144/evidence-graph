.PHONY: setup up down clean build

setup:
	cp .env.example .env

up:
	docker compose up -d

down:
	docker compose down

down-v:
	docker compose down -v

build:
	docker compose build

logs:
	docker compose logs -f
