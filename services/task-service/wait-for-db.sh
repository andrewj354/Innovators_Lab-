#!/bin/bash
# Wait for PostgreSQL database to be ready

set -e

host="$1"
user="$2"
password="$3"
dbname="$4"
shift 4
cmd="$@"

until PGPASSWORD=$password psql -h "$host" -U "$user" -d "postgres" -c '\q' 2>/dev/null; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

# Try to create database if it doesn't exist
PGPASSWORD=$password psql -h "$host" -U "$user" -d "postgres" -c "CREATE DATABASE IF NOT EXISTS $dbname;" 2>/dev/null || true

exec $cmd
