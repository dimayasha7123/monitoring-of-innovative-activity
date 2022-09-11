start:
	python manage.py runserver

run_redis:
	sudo docker run -d --name screenshots -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

stop_redis:
	sudo docker container stop screenshots
	sudo docker container rm screenshots