#!/bin/bash

type=$1
fails=""

# inspect() is used to calculate the number of failures
inspect() {
    if [ $1 -ne 0 ]; then
        fails="${fails} $2"
    fi
}

# Run server side tests
server() {
    docker-compose -f docker-compose-dev.yml up -d --build
    docker-compose -f docker-compose-dev.yml exec users python manage.py cov
    inspect $? users
    docker-compose -f docker-compose-dev.yml exec users flake8 project
    inspect $? users-lint
    docker-compose -f docker-compose-dev.yml down
}

# Run client side tests
client() {
    docker-compose -f docker-compose-dev.yml up -d --build
    docker-compose -f docker-compose-dev.yml exec client npm test -- --coverage
    inspect $? client
    docker-compose -f docker-compose-dev.yml down
}

# Run end to end tests
e2e() {
    docker-compose -f docker-compose-prod.yml up -d --build
    docker-compose -f docker-compose-prod.yml exec users python manage.py recreate_db
    ./node_modules/.bin/cypress run --config baseUrl=http://localhost # by default cypress run, runs tests headlessly, i.e. does not open up the browser
    inspect $? e2e
    docker-compose -f docker-compose-prod.yml down
}

# Run all tests
all() {
    docker-compose -f docker-compose-dev.yml up -d --build
    docker-compose -f docker-compose-dev.yml exec users python manage.py cov
    inspect $? users
    docker-compose -f docker-compose-dev.yml exec users flake8 project
    inspect $? users-lint
    docker-compose -f docker-compose-dev.yml exec client npm test -- --coverage
    inspect $? client
    docker-compose -f docker-compose-dev.yml down
    e2e
}

# run appropriate tests
if [[ "${type}" == "server" ]]; then
    echo "\n"
    echo "Running server-side tests!\n"
    server
elif [[ "${type}" == "client" ]]; then
    echo "\n"
    echo "Running client-side tests!\n"
    client
elif [[ "${type}" == "e2e" ]]; then
    echo "\n"
    echo "Running e2e tests!\n"
    e2e
else
    echo "\n"
    echo "Running all tests!\n"
    all
fi

# return proper code
if [ -n "${fails}" ]; then
    echo "\n"
    echo "Tests failed: ${fails}"
    exit 1
else
    echo "\n"
    echo "Tests passed!"
    exit 0
fi