FROM python:3.9

COPY ./ecommerce /srv/www/ecommerce
WORKDIR /srv/www/ecommerce

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt