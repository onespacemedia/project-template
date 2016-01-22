#!/bin/sh
python /app/manage.py collectstatic --noinput

NUM_WORKERS=`expr 2 \* \`cat /proc/cpuinfo | grep processor | wc -l\` + 1`
/usr/local/bin/gunicorn {{ cookiecutter.package_name }}.wsgi -w $NUM_WORKERS -b 127.0.0.1:5000 --chdir=/app
