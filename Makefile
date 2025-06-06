DOCKER_COMPOSE=app/.dev/docker-compose.yml
DOCKER_COMPOSE_TEST=app/.dev/docker-compose-test.yml
ALEMBIC_INI=alembic.ini

.PHONY: up down restart reset-db logs status

db-up:
	docker compose -f $(DOCKER_COMPOSE) up -d

db-down:
	docker compose -f $(DOCKER_COMPOSE) down

db-reset-db:
	docker compose -f $(DOCKER_COMPOSE) down -v

db-restart:
	make down
	make up

db-ogs:
	docker compose -f $(DOCKER_COMPOSE) logs -f

db-status:
	docker compose -f $(DOCKER_COMPOSE) ps

migrate-up:
	alembic -c $(ALEMBIC_INI) upgrade head

migrate-down:
	alembic -c $(ALEMBIC_INI) downgrade -1

tdb-up:
	docker compose -f $(DOCKER_COMPOSE_TEST) up -d

tdb-down:
	docker compose -f $(DOCKER_COMPOSE_TEST) down -v

tdb-run:
	pytest --cov=app --cov-report=term-missing

docker-kill-em-all:
	docker container stop $$(docker container ls -aq) || true
	docker container rm $$(docker container ls -aq) || true
	docker volume rm $$(docker volume ls -q) || true
	docker network rm $$(docker network ls -q | grep -v '^bridge$$' | grep -v '^host$$' | grep -v '^none$$') || true
	docker image rm $$(docker image ls -aq) || true

lint:
	ruff check . --fix
	black .

format:
	black .
	ruff format .

check:
	ruff check .
	black --check .