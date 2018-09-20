#!/bin/bash

fails=""

# inspect() is used to calculate the number of failures
inspect() {
    if [ $1 -ne 0 ]; then
        fails="${fails} $2"
    fi
}

# Run unit and integration tests
docker-compose -f docker-compose-dev.yml up -d --build
docker-compose -f docker-compose-dev.yml run users python manage.py test
inspect $? users
docker-compose -f docker-compose-dev.yml run users flake8 project
inspect $? users-lint
docker-compose -f docker-compose-dev.yml run client npm test -- --coverage
inspect $? client
docker-compose -f docker-compose-dev.yml down

# Return the appropriate code based on success/failure
if [ -n "${fails}" ]; then
    echo "Tests failed: ${fails}"
    exit 1
else
    echo "Test passed!"
    exit 0
fi