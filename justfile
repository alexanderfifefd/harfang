run:
    python3 manage.py runserver

open:
    open "http://localhost:8000"

css:
    npx tailwindcss -i static/css/input.css -o static/css/output.css --watch

up:
    docker build -t harfang -f Dockerfile .
    docker-compose up -d

down:
    docker-compose down

c-migrate:
    docker-compose exec app python manage.py makemigrations
    docker-compose exec app python manage.py migrate
    docker-compose exec app python manage.py migrate --database clickhouse

clickhouse:
    docker-compose exec -it clickhouse clickhouse-client

flower:
    open "http://localhost:5555/"

migrate:
    python3 manage.py makemigrations
    python3 manage.py migrate

populate: rm-migrations migrate
    python3 manage.py setup_test_data

setup:
    pip3 install -r requirements.txt
    pre-commit install
    python3 manage.py makemigrations

rm-migrations:
    #!/usr/bin/env bash
    echo "Removing migrations..."
    find . -path "*/migrations/0*.py" -delete 2> /dev/null
    find . -path "*/migrations/__pycache__" -delete 2> /dev/null
    echo "Removing database..."
    rm -f db.sqlite3 2> /dev/null
