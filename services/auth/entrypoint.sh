if [ "$DB_NAME" = "auth_service" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

export PYTHONPATH=$(pwd):$PYTHONPATH

echo "Applying migrations..."
alembic upgrade head

echo "Start Auth Service"
python src/main.py