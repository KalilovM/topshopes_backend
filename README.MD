<!-- Simple project overview -->

## Overview

It's a simple marketplace for selling and buying products. For now, it's only a backend part of the project.
Functionality:

- User registration
- User login
- User logout
- User profile update, change, delete, create
- Product creation, update, delete
- Shop creation, update, delete
- Static pages (about, contacts, etc.)
- Static pages categories and navigation
- Admin panel for managing users, products, shops, static pages, etc.
  Available Commands:
- python manage.py fill_dummy - fill database with dummy data (Wouldn't fill navigation and static pages)
- python manage.py createsuperuser - create superuser

## Installation

- Clone the repository
- Create virtual environment
- Install requirements
- Create .env file in the root directory of the project (in progress)
- Fill .env file with your data
- Run migrations
- Run server

## .env file (in progress)

- SECRET_KEY - Django secret key
- DEBUG - Debug mode (True or False)
- ALLOWED_HOSTS - Allowed hosts
- DB_ENGINE - Database engine (django.db.backends.postgresql_psycopg2)
- DB_NAME - Database name
- DB_USER - Database user
- DB_PASSWORD - Database password
- DB_HOST - Database host
- DB_PORT - Database port
- EMAIL_HOST - Email host
- EMAIL_PORT - Email port
- EMAIL_HOST_USER - Email host user
- EMAIL_HOST_PASSWORD - Email host password
- EMAIL_USE_TLS - Email use TLS (True or False)
- EMAIL_USE_SSL - Email use SSL (True or False)
- DEFAULT_FROM_EMAIL - Default from email
- SERVER_EMAIL - Server email
- EMAIL_BACKEND - Email backend (django.core.mail.backends.smtp.EmailBackend)
- STATIC_ROOT - Static root
- MEDIA_ROOT - Media root
- MEDIA_URL - Media url
- STATIC_URL - Static url

## TODO

- User roles
- Setting up .env file
- Configuring Swagger
- Tests
- Configuring PostgreSQL
- Configuring gunicorn
- Configuring nginx
- Configuring Docker
- Configuring CI/CD
- Configuring Redis
- Configuring Celery
- Configuring Hostinger.com
