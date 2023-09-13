FROM python:3.11.5-slim-bullseye

WORKDIR /ecommerce

COPY . /ecommerce

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
