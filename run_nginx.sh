#!/bin/bash

./manage.py collectstatic --noinput
nginx -g "daemon off;"
