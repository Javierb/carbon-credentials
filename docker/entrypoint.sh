#!/usr/bin/env sh

set -o errexit
set -o nounset

cmd="$*"

postgres_ready () {
  # Check that postgres is up and running on port `5432`:
  sh '/wait-for.sh' -t 3 ${SQL_HOST}:${SQL_PORT}
}

# We need this line to make sure that this container is started
# after the one with postgres:
until postgres_ready; do
  >&2 echo 'Postgres is unavailable - sleeping'
done

# It is also possible to wait for other services as well: redis, elastic, mongo
>&2 echo 'Postgres is up - continuing...'

>&2 echo "Applying database migrations"
python manage.py migrate

>&2 echo "Starting django dev server"
python manage.py runserver 0.0.0.0:8000

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd