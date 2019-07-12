# Carbon Credentials Assignment

## Requirements
[Docker and Docker Compose](https://docs.docker.com/compose/install/)

## Quick start
Clone the repository from github and start the services with docker compose.

``git clone https://github.com/Javierb/carbon-credentials.git``

``cd carbon-credentials``

``docker-compose up``

- Navigate to: [http://localhost:8000/](http://localhost:8000/)
- To access the django admin site:
  - create a superuser by running ``docker-compose run web python manage.py createsuperuser`` and create your credentials.
  - browse to: [http://localhost:8000/admin/](http://localhost:8000/admin/) and login with your credentials.
- To run the tests ``docker-compose run web python manage.py test``
- RabbitMQ web client is accessible on ``http://localhost:15672/`` with ``user: guest and password: guest``

## Back-end tech stack
- Docker & docker-compose
- Python 3.7
- Django 2.2
- django-import-export
- Django Rest Framework 3
- Postgres
- Celery
- RabbitMQ

## Front-end stack
- Bootstrap
- JQuery
- ChartistJS

## Features
- CSV import: Async import with Celery and RabbitMQ. Also in the Admin side there is an import export integration of django-impor-export (It's syncronous and will time out for large files).
- Data display for the 3 models
- Simple chart: Asyncronously the front-end gets the data from a REST end point and displays a daily aggregation of consumption per meter. 

## Possible improvements
- Cosmetic improvements.
- Front-end framework integration.
- Optimization of static files, compresing.
- Production environment + Proxy server to serve static files
