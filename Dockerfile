FROM python:3.9

WORKDIR /ecommerce

COPY . /ecommerce

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
