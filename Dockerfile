FROM python:3.9.5-slim

WORKDIR chart/src/app

RUN pip install --upgrade pip

# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1
# Installing database driver to get django app access to connect to PostgreSQL...
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# ENTRYPOINT python manage.py runserver


