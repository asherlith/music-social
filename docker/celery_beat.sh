#!/bin/sh

cd /app/music_social/

rm -rf /tmp/celerybeat.pid
celery -A music_social beat -l info --pidfile=/tmp/celerybeat.pid
