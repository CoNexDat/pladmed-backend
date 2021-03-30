# Pladmed backend

#### How to run
You can run everything through Docker:

- make start: Starts the server
- make debug: Starts the server and watch for logs
- make logs: See logs of the server
- make stop: Stops the server
- make test: Run the tests

Accessible (default) at http://localhost:5000/

#### Configuration
If you want to use the database that is included in docker-compose, you must set its parameters in file `.env_database`:
```
MONGO_INITDB_DATABASE=<database-name:pladmed> # Database name
MONGO_INITDB_ROOT_USERNAME=<database-root-user> # Root database user
MONGO_INITDB_ROOT_PASSWORD=<database-password> # Database password
```
Then, to set the server properties you should create the `.env_server` file, containing these environment properties:
```
PYTHONUNBUFFERED=1 # Ensures the python output is sent directly to the container log

DEBUG=1 # Debug level
PORT=<app_port:5000> # Used port
HOST=<app_host:0.0.0.0> # The server host 
FLASK_ENV=<development|production> # Execution environment
FLASK_APP=main.py # Required to init Flask application

SECRET_KEY=<secret-key-for-tokens> #Secret key used for token generation

DATABASE=mongo

MONGO_USERNAME=<database-root-user> # Databse user
MONGO_PASSWORD=<database-password> #Databse user password
MONGO_DATABASE=<database-name:pladmed> #Databse name
MONGO_HOST=<mongo-host:db> #Database host
MONGO_PORT=<mongo-port:27017> #Database port

LOG_FILE=server.log #Log file
```

#### Architecture
##### Robustness and system characteristics
This diagram show the system robustness. First, we have the actors that can trigger events through an endpoint. This triggers actions in any of the nodes, which are connected to a MongoDB databasefor data persistency and to Chrony for time synchronization. If needed, serves communicate with the clients through sockets.
 ![Robustness diagram](docs/robustez-pladmed.png)
 
##### Deploy
Now, let's see the system deploy. We have the different clients that will run the frontend app in their own browrsers. Also, every client can run a probe (See [probe documentation](https://github.com/fedefunes96/pladmed-client) for installation guide).
 ![Deploy diagram](docs/despliegue.png)

In this scenario, "coordination servers" are those which run the server, do the time coordination and measurements. Different clients make requests to the server through the frontend app or the probes.

##### Time synchronization
Time synchronization is achieved via Chrony, using it as a NTP client. Also, the server works as a NTP server for probe time synchronization, so we don't overload public servers.
Out system has this stratum diagram:
 ![NTP Diagram](docs/time-sync.png)
 
We can see that NTP servers are part of p-stratum. So, out server will be part of p+1-stratum. As it works as a NTP server, the probes will be part of p+2-stratum.
 
#### Endpoints 
Inside directory `docs/endpoints` you will find the .yaml file that will serve as input for Swagger and check every available endpoint.
