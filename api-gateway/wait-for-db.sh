#!/bin/bash
set -e

host="$1"
user="$2"
password="$3"
database="$4"

shift 4

until PGPASSWORD=$password psql -h "$host" -U "$user" -d "$database" -c "\q" 2>/dev/null; do
  >&2 echo "Postgres $database is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres $database is up - executing command"
exec "$@"
