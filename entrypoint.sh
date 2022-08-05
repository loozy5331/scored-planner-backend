# django's entrypoint

postgres_ready() {
    $(which curl) http://$DBHOST:$DBPORT/ 2>&1 | grep '52'
}

until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available.'

python manage.py migrate
python manage.py runserver 0.0.0.0:8000