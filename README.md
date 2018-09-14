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

## Run the app with Docker Compose

To run and build the application locally (in development mode), cd into the root directory and type the following command:

        $ docker-compose -f docker-compose-dev.yml up -d --build

The above command will build and run the application, in the background (because of the ```-d``` flag) and not show any debug output. To show the debug output (which might be preferrable, incase the app crahses) remove the ```-d``` flag from the command above.

Once the command is executed, you can access the app at the following link: [http://localhost:5001/users/ping]("http://localhost:5001/users/ping").

## Creating a database for Testing

This application is composed of a few services which all depend on their individual databases. To test the ```users``` service, you can first create a ```users``` database, from the command line, by using this command (at the root of the app):

        $ docker-compose -f docker-compose-dev.yml run users python manage.py recreate_db

## Testing the app

The app was developed using the principles of TDD. To run the tests for the ```users``` service, cd into the root directory of the app and run the following command:

        $ docker-compose -f docker-compose-dev.yml run users python manage.py test

To run the tests for the ```client``` service, cd into the root directory of the app and run the following command:

        $ docker-compose -f docker-compose-dev.yml run client npm test 

## Test Coverage

For test coverage, this project uses ```Coverage.py```. To find out how much test coverage the app has, run the following command:

        $ docker-compose -f docker-compose-dev.yml run users python manage.py cov
        
## Seeding the database

Sometimes it might be helpful to seed the database with some initial data during development in order to get some useful response. This can be done from the command line using the following command:

        $ docker-compose -f docker-compose-dev.yml run users python manage.py seed_db

## Data Migration

The data migration steps are as follows:

        $ docker-compose -f docker-compose-dev.yml run users python manage.py db migrate

        $ docker-compose -f docker-compose-dev.yml run users python manage.py db upgrade

## Permissions

The commands above may not run if the correction permissions are not set. Below are some of the permissions that need to be set to ensure the app builds and runs according to the commands above:

        $ chmod +x entrypoint.sh

The above command should be run from the root of ```services/users/```.

## Code Quality

For ensure good code quality according to ```pep8``` standards, this project uses ```Flake8``` for linting. The linting tests are also run as part of the continous integration pipeline with Travis.