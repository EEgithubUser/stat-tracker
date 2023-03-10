#!/bin/sh

flask db upgrade

exec gunicorn --bind 0.0.0.0:80 "__init__:create_app()"