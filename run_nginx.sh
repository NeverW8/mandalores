#!/bin/bash

chmod -R 755 /mandalores/static
find /mandalores/static -type f -exec chmod 644 {} \;
chown -R nginx:nginx /mandalores/static


./manage.py collectstatic --noinput

nginx -g "daemon off;"
