#!/bin/bash

./manage.py migrate
gunicorn -b 0.0.0.0:5000 mandalores.wsgi --workers=3
