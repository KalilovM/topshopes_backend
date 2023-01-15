FROM python:3.11
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

ENV PYTHONUNBUFFERED 1

RUN mkdir /backend

WORKDIR /backend

ADD . /backend/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000