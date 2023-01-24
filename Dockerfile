FROM python:3.11.1-bullseye


WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
# EXPOSE 8000

RUN chmod +x /backend/entrypoint.sh
ENTRYPOINT ["sh","/backend/entrypoint.sh"]
# CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000