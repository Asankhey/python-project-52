install:
	uv pip install -r requirements.txt

run:
	python manage.py runserver

migrate:
	python manage.py migrate

createsuperuser:
	python manage.py createsuperuser

collectstatic:
	python manage.py collectstatic --noinput

render-start:
	gunicorn task_manager.wsgi

build:
	./build.sh