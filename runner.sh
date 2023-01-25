#!/bin/zsh

# Run migrations

python manage.py makemigrations attributes head orders pages posts products reviews roles shops sliders users applications payments
python manage.py migrate

# Run server

python manage.py runserver