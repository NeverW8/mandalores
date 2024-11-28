#!/bin/bash

./manage.py collectstatic --noinput

chmod -R 755 /mandalores/static
find /mandalores/static -type f -exec chmod 644 {} \;
chown -R nginx:nginx /mandalores/static

nginx -g "daemon off;"

