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
docker-compose -f docker-compose-dev.yml exec users python manage.py test
inspect $? users
docker-compose -f docker-compose-dev.yml exec users flake8 project
inspect $? users-lint
docker-compose -f docker-compose-dev.yml exec client npm test -- --coverage
inspect $? client
docker-compose -f docker-compose-dev.yml down

# Run the end-to-end (e2e) tests
docker-compose -f docker-compose-prod.yml up -d --build
docker-compose -f docker-compose-prod.yml exec users python manage.py recreate_db
./node_modules/.bin/cypress run --config baseUrl=http://localhost # by default cypress run, runs tests headlessly, i.e. does not open up the browser
inspect $? e2e
docker-compose -f docker-compose-prod.yml down

# Return the appropriate code based on tests success/failure
if [ -n "${fails}" ]; then
    echo "Tests failed: ${fails}"
    exit 1
else
    echo "Test passed!"
    exit 0
fi