#!/bin/bash

./manage.py migrate
gunicorn --config=/mandalores/gunicorn.py \
  -b 0.0.0.0:5000 \
  mandalores.wsgi \
  --workers=3 \
  --capture-output \
  --log-file=- \
  --access-logfile=- \
  --error-logfile=- \
  --forwarded-allow-ips="*" 2>&1
