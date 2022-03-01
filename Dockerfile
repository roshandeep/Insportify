
FROM python:3.8.5

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

# CMD ["gunicorn"  , "--bind","0.0.0.0:8000", "connex.wsgi:application","--workers 3"]

# CMD python manage.py runserver
