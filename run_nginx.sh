#!/bin/bash

./manage.py collectstatic --noinput
chmod 755 /mandalores/static
chmod 644 /mandalores/static/*
nginx -g "daemon off;"
