run:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py createsuperuser

redis_start:
	docker run --name redis-celery -p 6379:6379 -d redis

celery_start:
	celery -A core worker --loglevel=info
