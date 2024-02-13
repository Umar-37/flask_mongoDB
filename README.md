# Flask and MongoDb sample app

## Start MongoDB

    docker run --rm --name mongodb -p 27017:27017 mongodb/mongodb-community-server:6.0-ubi8

## Start flask

    flask --app blog run --debug

## User commands

    # Create new user
    flask --app blog users_admin create newuser
    # Reset user password
    flask --app blog users_admin reset currentuser
    # Fake blog data
    flask --app blog posts_admin seed_test_data


## Todos

- user env for connection info and secret
- flash messages everywhere
- paging

## MongoDb

- indexies
    - explain
    - full text
    - geo
- aggregation
- compass
