update-requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

compose-run:
	docker-compose up --build

compose-run-databases:
	docker-compose up database redis

compose-restart-app:
	docker-compose restart app

alembic-clear:
	rm -rf alembic/versions/*

alembic-cm:
	poetry run alembic revision --autogenerate

alembic-migrate:
	poetry run alembic upgrade head
