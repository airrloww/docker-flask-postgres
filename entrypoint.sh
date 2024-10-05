#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

if [ ! -d "migrations" ]; then
  echo "Initializing Flask-Migrate..."
  flask db init
fi

flask db migrate -m "Generated migration"

flask db upgrade

exec flask run --host=0.0.0.0
