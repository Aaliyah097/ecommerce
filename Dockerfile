FROM python

WORKDIR /ecommerce

COPY . /ecommerce

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

# CMD ["gunicorn", "--bind", "0.0.0.0:8001","ecommerce.wsgi:application"]
