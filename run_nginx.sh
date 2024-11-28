#!/bin/bash

chmod -R 755 /mandalores/static
find /mandalores/static -type f -exec chmod 644 {} \;

./manage.py collectstatic --noinput

nginx -g "daemon off;"

