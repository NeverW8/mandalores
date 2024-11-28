#!/bin/bash

chmod 755 /mandalores/static
chmod 644 /mandalores/static/*
nginx -g "daemon off;"
./manage.py collectstatic --noinput
