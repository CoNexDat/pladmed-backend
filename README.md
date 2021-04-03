# Pladmed backend

[![Build Status](https://travis-ci.com/fedefunes96/pladmed-backend.svg?branch=travis-badge)](https://travis-ci.com/fedefunes96/pladmed-backend)

[![codecov](https://codecov.io/gh/fedefunes96/pladmed-backend/branch/master/graph/badge.svg?token=YTU6E27H7T)](https://codecov.io/gh/fedefunes96/pladmed-backend)

- [Pladmed backend](#pladmed-backend)
  - [How to run locally](#how-to-run-locally)
  - [Configuration](#configuration)
  - [Endpoints / pladmed-backend web API documentation](#endpoints--pladmed-backend-web-api-documentation)
  - [Additional documentation](#additional-documentation)

## How to run locally
You can run everything through Docker:

- make start: Starts the server
- make debug: Starts the server and watch for logs
- make logs: See logs of the server
- make stop: Stops the server
- make test: Run the tests

Accessible (default) at http://localhost:5000/

## Configuration

To configure the Mongo database that will run in a separate Docker container via docker-compose, a file named `.env_database` will need to be created at the repository's root level. This file will contain the environment variables for configuring the database container. See `.env_database.example` for the default values.

```
MONGO_INITDB_DATABASE=<database-name:pladmed> #Database name
MONGO_INITDB_ROOT_USERNAME=<database-root-user> #root user for this database
MONGO_INITDB_ROOT_PASSWORD=<database-password> #root user password
```

Similarly, to configure the server itself, a file named `.env_server` will need to exist at the root level. It will need to contain the following environment variables:

```
PYTHONUNBUFFERED=1 #Needed to send logs to container

DEBUG=1 #Debug level
PORT=<app_port:5000> #TCP port (internal to Docker where the server will listen for requests)
HOST=<app_host:0.0.0.0> #IP address, internal to Docker network, where the server will run
FLASK_ENV=<development|production> #Define execution environment
FLASK_APP=main.py #Required by Flask framework

SECRET_KEY=<secret-key-for-tokens> #Used to generate security tokens

DATABASE=mongo

MONGO_USERNAME=<database-root-user> #root user for connecting to database
MONGO_PASSWORD=<database-password> #root user password
MONGO_DATABASE=<database-name:pladmed> #Mongo database name
MONGO_HOST=<mongo-host:db> #Database host
MONGO_PORT=<mongo-port:27017> #Database service port

LOG_FILE=server.log #Log file location
```
## Endpoints / pladmed-backend web API documentation

Inside the  `docs/endpoints` directory, there's a .yaml [Swagger](https://swagger.io/tools/swagger-ui/) file which can be used for viewing and testing the web API endpoints.

Alternatively, in the same directory, there is a [Postman](https://www.postman.com/) collection, which can be imported and used in Postman.

## Additional documentation

- [Architecture](docs/architecture.md)
- [Class diagram and class responsibilites](docs/class-diagram.md)
- [Deployment/installation](docs/deployment.md)
- [Time synchronization](time-sync.md)
