# piedpiperproject
mystery....

### Размышления на тему

[System design](https://miro.com/app/board/uXjVO5bzoxc=/?share_link_id=321204215848)

### Запуск

Как запустить (надеюсь для этого в будущем будет docker-compose):
1. Поднимаем Redis при помощи Docker
```
docker run -d --name screenshots -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```
2. Ставим Python (не забываем про pip). Можно [отсюда](https://www.python.org/downloads/).
3. Подтягиваем зависимости. Заходим в папку с проектом и оттуда просим pip'a:
```
pip install -r requirments.txt
```
3. Запускаем сервер (также находясь в корне проекта):
```
py -3 manage.py runserver

// или

python manage.py runserver
```
