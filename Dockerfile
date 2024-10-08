FROM ubuntu:latest

RUN apt-get update && apt-get -y install cron && apt-get -y install pip

# Instala las dependencias necesarias para compilar psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    gcc

RUN touch /var/log/cron.log

RUN (crontab -l ; echo "* * * * * echo 'Hello world' >> /var/log/cron.log") | crontab

CMD cron && tail -f /var/log/cron.log

WORKDIR /usr/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/app/requirements.txt
RUN pip install --break-system-packages -r requirements.txt
