# MicroServiceTDD

[![Build Status](https://travis-ci.com/aljoshb/microservices_app_docker_flask_react.svg?branch=master)](https://travis-ci.com/aljoshb/microservices_app_docker_flask_react)

## Introduction

This project is a code evaluation web application that allows users to take coding exercises and get graded instantly on their performance.

This web application is architected in a microservices fashion and is built using Docker, Flask and React and deployed to AWS. I built this application using test-driven development (TDD) principles by writing tests before writing the code that the tests are for.

## Installation Requirements

This project uses Docker for development and deployment to AWS (EC2 instance), so it is important that Docker is installed on the development machine.

## Tech Stack

This is quite a large project and as a result, it uses a lot of tools and technologies to power the app. At a high level, the project uses Flask, Docker and React.

Digging a bit deeper, you'll find that the project uses the following:

```Python, Flask, Flask-SQLAlchemy, PostgreSQL, Flask-Testing, Gunicorn, Nginx, Docker, Docker Compose, Docker Machine, Flask Blueprints, Jinja Templates, Travis (CI), Node, Create React App, React, Enzyme, Jest, Axios, Flask-CORS, React forms, Flask Debug Toolbar, Flask-Migrate, Flask-Bcrypt, PyJWT, react-router-dom, Bulma, React Authentication and Authorization, Cypress, Swagger UI, AWS, EC2, Elastic Container Registry (ECR), Elastic Container Service (ECS), Elastic Load Balancing (ELB), Application Load Balancer (ALB), Relational Database Service (RDS), AWS Lambda and API Gateway, AWS Lambda and ECS, PropTypes```

## Run the app with Docker Compose Locally

NOTE: You need to ensure that ```users``` database has been created first, so if this is the first time starting up the containers (after taking them down), complete the ```Creating a database for Manual Development Testing``` and ```Seeding the database``` sections.

To run and build the application locally (in development mode), cd into the root directory and type the following command:

        $ docker-compose -f docker-compose-dev.yml up -d --build

The above command will build and run the application, in the background (because of the ```-d``` flag) and not show any debug output. To show the debug output (which might be preferrable, incase the app crahses) remove the ```-d``` flag from the command above. By "run the application", I mean the command will create all the containers, and run the default commands specified in the docker files of the container's images.

At this point, the databases will have been created (i.e. `users_dev`, `users_prod` and `users_test`) because there were specified in the `user-db` service `Dockerfile`. However, the actual tables in these databases will not have been created, since there is no command in the application code that actually creates the database (for instance, no `db.create_all()` command in the `users` service code, which is needed to create the tables).

Therefore, you will need to run the database migrations on the application. The migration scripts have already been created, so to apply them use the following command:

        $ docker-compose -f docker-compose-dev.yml exec users python manage.py db upgrade

Note that `exec` is used since this assumes you have already ran the above command and the `users` container is running.

Once application is running and the migrations have been executed, you can access the app at the following links: [http://localhost:5001/users/ping]("http://localhost:5001/users/ping") and [http://localhost]("http://localhost"). Trying to access these links without running the migration will lead to an internal server error, since the `users` relation (i.e. table) has not yet been created.

## Creating a database for Manual Development Testing

This application is composed of a few services which all depend on their individual databases. To test the ```users``` service, you can first create a ```users``` database, from the command line, by using this command (at the root of the app):

        $ docker-compose -f docker-compose-dev.yml run users python manage.py recreate_db

## Seeding the database

Sometimes it might be helpful to seed the database with some initial data during development in order to get some useful response. This can be done from the command line using the following command:

        $ docker-compose -f docker-compose-dev.yml run users python manage.py seed_db

# Get into psql manually

To get into psql manually, run the following command:

        $ docker-compose -f docker-compose-dev.yml exec users-db psql -U postgres

You can then connect to a database, for instance, to connect to the development database:

        # \c users_dev

To view the tables in the ```users_dev``` database:

        # \d users

To exit from the psql REPL:

        # \q

## Testing the app

The app was developed using the principles of TDD. To run the tests for the ```users``` service, cd into the root directory of the app and run the following command:

        $ docker-compose -f docker-compose-dev.yml run users python manage.py test

To run the tests for the ```client``` service, cd into the root directory of the app and run the following command:

        $ docker-compose -f docker-compose-dev.yml run client npm test

### Testing Script

To run all the unit and integration tests, run the ```test.sh``` script from the root of the repository as follows:

        $ sh test.sh

To run only the server side tests:

        $ sh test.sh server

To run only the client side tests:

        $ sh test.sh client

To run only the end to end tests:

        $ sh test.sh e2e

You can also run the ```test.sh``` script using the following command:

        $ ./test.sh

Only after granting permission by doing:

        $ chmod +x ./test.sh

### Test Coverage

For test coverage, this project uses ```Coverage.py``` to test the python applications. To run test coverage on the ```users``` service:

        $ docker-compose -f docker-compose-dev.yml run users python manage.py cov

To run test coverage on the ```client``` service, this project uses ```npm```'s built in test coverage option:

        $ docker-compose -f docker-compose-dev.yml run client npm test -- --coverage

NOTE: Running the ```test.sh``` script will run all these tests and more. This section is just to show you how to run it manually on your own.

### End to End Testing with Cypress

For the end to end test, ```crypress``` is used. ```cypress``` is a desktop application that can be used to test anything that runs in the browser.

To get started, create a ```package.json``` file in the root folder of the application, install ```crypress``` as a ```dev-dependency```:

        $ npm install cypress@3.0.1 --save-dev

Then open the Cypress test runner desktop app:

        $ ./node_modules/.bin/cypress open

From the Crypress test runner app, you can run all the tests. But, ensure that the ```baseUrl``` field is set to ```http://localhost``` in the ```crypress.json``` configuration file.

## Database Migration

The database migration steps are as follows:

        $ docker-compose -f docker-compose-dev.yml run users python manage.py db migrate

        $ docker-compose -f docker-compose-dev.yml run users python manage.py db upgrade

## Permissions

The commands above may not run if the correction permissions are not set. Below are some of the permissions that need to be set to ensure the app builds and runs according to the commands above:

        $ chmod +x entrypoint.sh

The above command should be run from the root of ```services/users/```.

## Code Quality

For ensure good code quality according to ```pep8``` standards, this project uses ```Flake8``` for linting. The linting tests are also run as part of the continous integration pipeline with Travis.

## Production vs Development docker machine

To point the docker client to the docker production machine, run the following commands:

        $ docker-machine env testdriven-prod
        $ eval $(docker-machine env testdriven-prod)

Also, you need to set the ```REACT_APP_USERS_SERVICE_URL``` environment variable:

        $ export REACT_APP_USERS_SERVICE_URL=http://DOCKER_MACHINE_IP

To point the docker client back to the local/development docker machine:

        $ eval $(docker-machine env -u)

Reset the ```REACT_APP_USERS_SERVICE_URL``` environment variable:

        $ export REACT_APP_USERS_SERVICE_URL=http://localhost
