FROM python:3.9
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
COPY . .
RUN pip install -r req.txt --no-cache-dir
ENTRYPOINT ["python", "manage.py", "runserver"]
