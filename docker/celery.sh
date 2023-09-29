#!/bin/sh

cd /app/music_social/

rm -rf /tmp/celeryd.pid
celery -A music_social worker -l info --pidfile=/tmp/celeryd.pid
