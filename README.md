# Carbon Credentials Assignment

## Requirements
[Docker and Docker Compose](https://docs.docker.com/compose/install/)

## Quick start
Clone the repository from github and start the services with docker compose.

``git clone https://github.com/Javierb/polestar.git``

``cd carbon-credentials``

``docker-compose up``

- Navigate to: [http://localhost:8000/](http://localhost:8000/)
- To browse the API go to: [http://localhost:8000/api/](http://localhost:8000/api/)
- To access the django admin site:
  - create a superuser by running ``docker-compose run web python manage.py createsuperuser`` and create your credentials.
  - browse to: [http://localhost:8000/admin/](http://localhost:8000/admin/) and login with your credentials.
- To run the tests ``docker-compose run web python manage.py test``

## Back-end tech stack
- Docker & docker-compose
- Python 3.7
- Django 2.2
- django-import-export
- Django Rest Framework 3
- Postgres

## Front-end stack
- Bootstrap
- JQuery
- ChartistJS

## Possible improvements
- Cosmetic improvements.
- Front-end framework integration. (i.e: React + Bootstrap).
- Sphinx documentation.

