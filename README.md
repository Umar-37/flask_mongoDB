# Flask and MongoDB sample blog app

## Installation
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

## Start MongoDB

    # NOTE: no presistant for data
    docker run --rm --name mongodb -p 27017:27017 mongodb/mongodb-community-server:6.0-ubi8

## Start flask

    flask --app blog run --port 5001 --debug

## User commands

    # Create new user
    flask --app blog users_admin create newuser
    # Reset user password
    flask --app blog users_admin reset currentuser
    # Seed fake posts
    flask --app blog posts_admin seed_test_data 10

## MongoDB Todos

- indexies
    - full text
