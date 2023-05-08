migrate:
	python manage.py makemigrations
	python manage.py migrate

redis_start:
	docker run --name redis-celery -p 6379:6379 -d redis

celery_start:
	celery -A core worker --loglevel=info

app_start:
	python manage.py runserver
