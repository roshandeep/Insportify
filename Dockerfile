
FROM python:3.8.5

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt


# COPY /app/nginx/insportify.com.crt
# ADD you_certificate.crt:/container/cert/path
RUN update-ca-certificates
RUN pip install -r requirements.txt

EXPOSE 8000
# EXPOSE 443

RUN python manage.py collectstatic --noinput
# CMD [ "python", "manage.py",  "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "Insportify.wsgi"]


# CMD ["gunicorn"  , "--bind","0.0.0.0:8000", "insportify.wsgi:application","--workers 3"]

# CMD python manage.py runserver
