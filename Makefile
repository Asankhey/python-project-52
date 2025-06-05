install:
	uv sync

build:
	./build.sh

start:
	uv run manage.py runserver localhost:8010

render-start:
	gunicorn task_manager.wsgi

check:
	uv run ruff check task_manager

check-fix:
	uv run ruff check --fix .

migrations:
	python manage.py makemigrations

migrations-user:
	python manage.py makemigrations user

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

translate-compile:
	django-admin compilemessages

translate-makemessages:
	django-admin makemessages -l ru

test:
	uv run manage.py test

tests-cov:
	uv run coverage run ./manage.py test
	uv run coverage xml