# Introduction

This project is a code evaluation web application that allows users to take coding exercises and get graded instantly on their performance.

This web application is architected in a microservices fashion and is built using Docker, Flask and React. I built this application using test-driven development (TDD) principles by writing tests before writing the code that the tests are for.

## Tech Stack

This is quite a large project and as a result, it uses a lot of tools and technologies to power the app. At a high level, the project uses Flask, Docker and React.

Digging a bit deeper, you'll find that the project uses the following:

```Python, Flask, Flask-SQLAlchemy, PostgreSQL, Flask-Testing, Gunicorn, Nginx, Docker, Docker Compose, Docker Machine, Flask Blueprints, Jinja Templates, Travis (CI), Node, Create React App, React, Enzyme, Jest, Axios, Flask-CORS, React forms, Flask Debug Toolbar, Flask-Migrate, Flask-Bcrypt, PyJWT, react-router-dom, Bulma, React Authentication and Authorization, Cypress, Swagger UI, AWS, EC2, Elastic Container Registry (ECR), Elastic Container Service (ECS), Elastic Load Balancing (ELB), Application Load Balancer (ALB), Relational Database Service (RDS), AWS Lambda and API Gateway, AWS Lambda and ECS, PropTypes```

## Run the app

To run and build the application locally, cd into the root directory and type the following command:

        $ docker-compose -f docker-compose-dev.yml up -d --build

The above command will build and run the application, in the background (because of the ```-d``` flag) and not show any debug output. To show the debug output (which might be preferrable, incase the app crahses) remove the ```-d``` flag from the command above.

Once the command is executed, you can access the app at the following link: [http://localhost:5001/users/ping]("http://localhost:5001/users/ping").

## Testing the app

The app was developed using the principles of TDD. To run the tests for the ```users``` service, cd into the root directory of the app and run the following command:

        $ docker-compose -f docker-compose-dev.yml run users python manage.py test

## Permissions

The commands above may not run if the correction permissions are not set. Below are some of the permissions that need to be set to ensure the app builds and runs according to the commands above:

        $ chmod +x entrypoint.sh

The above command should be run from the root of ```services/users/```.