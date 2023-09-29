FROM python:3.11


WORKDIR /app


COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt


COPY docker/celery.sh /app/docker/celery.sh
RUN chmod +x /app/docker/celery.sh

COPY docker/celery.sh /app/docker/celery_beat.sh
RUN chmod +x /app/docker/celery_beat.sh

ADD music_social /app/music_social

ENV PYTHONUNBUFFERED 1



