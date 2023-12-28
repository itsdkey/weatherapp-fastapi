# Weather app using FastAPI

* [Intuition](#intuition)
* [What I used](#what-i-used)
* [What patterns I followed](#what-patterns-i-followed)
* [Local development](#local-development-using-virtualenv)
    * [Env vars setup](#env-vars-setup)
    * [InfluxDB setup](#influxdb-setup)
    * [using docker compose](#local-development-using-docker-compose)
* [Project conventions](#project-conventions)

## Intuition
Just a fun project to code a simple weather app. However, I wanted to get more familiar
with new technologies such as:
- [FastAPI](https://fastapi.tiangolo.com/)
- [InfluxDB](https://www.influxdata.com/)
- [pytest](https://github.com/pytest-dev/pytest)
- [Pydantic](https://docs.pydantic.dev/latest/)


## What I used
To learn something about the technologies (follow some conventions mentioned in their
documentations) and also to follow best practices I used the following concepts:
- [env vars](https://fastapi.tiangolo.com/advanced/settings/#environment-variables)
for WeatherClient domain and API Key (so we can change and for security reasons),
- [Use FastAPI's Settings Object](https://fastapi.tiangolo.com/advanced/settings/#create-the-settings-object) to load env vars into our FastAPI app
- [InfluxDB Python client](https://github.com/influxdata/influxdb-client-python?tab=readme-ov-file#delete-data) to connect with our InfluxDB
- [App separation](https://fastapi.tiangolo.com/tutorial/bigger-applications/) so our project has a nice structure
- [Path parameters](https://fastapi.tiangolo.com/tutorial/path-params/?h=enum#path-parameters)
- [Query parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
- [How-To for NoSQL DBs](https://fastapi.tiangolo.com/how-to/nosql-databases-couchbase/) a recipe how to connect with a NoSQL Database in FastAPI

## What patterns I followed
To keep following the best practices and to have my code more structured I decided to follow the patterns below:
- A Client class for 3rd party integration - so the code responsible for requesting 3rd parties is separated from the rest
- [Adapter design pattern](https://refactoring.guru/design-patterns/adapter) - so I can convert the 3rd party response the way I want it to be used by my app
- dataclasses - thanks to Pydantic I could use real objects instead of plain dictionaries.

## Env vars setup
To make this project work you first need to set up the required env vars:
* OPENWEATHER_API_KEY
* OPENWEATHER_DOMAIN
* INFLUXDB_ORG=< your InfluxDB organization >
* INFLUXDB_BUCKET=< your InfluxDB initial bucket >
* INFLUXDB_URL=http://influxdb:8086  (becasue we will create a connection between containers)
* INFLUXDB_TOKEN=<your InfluxDB token that will be used for DB connection/queries)

You can receive the openweather values from your openweather account on https://home.openweathermap.org/api_keys
# InfluxDB setup
To set up your InfluxDB instance (using docker compose) first you need to create a separate env file called `.infludb2.env` and fill the values for:
DOCKER_INFLUXDB_INIT_MODE=setup
DOCKER_INFLUXDB_INIT_USERNAME=<admin's username>
DOCKER_INFLUXDB_INIT_PASSWORD=<admin's password>
DOCKER_INFLUXDB_INIT_ORG=<your InfluxDB init organization>
DOCKER_INFLUXDB_INIT_BUCKET=<your InfluxDB initial bucket>
DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=<your admin init token>

After that when you run the container and enter: http://127.0.0.1:8086/ you should see the InfluxDB logindashboard. After a
successful login you can follow the "getting-started" tutorial.


## Local development using docker compose
Build and the application with the following:
```shell
docker compose up app
```
You can run it in the background if you use the `-d` flag:
```shell
docker compose up -d app
```


## Project conventions
The project follows some specific conventions thanks to pre-commit:
- isort
- black
- flake8
- no-commit-to-branch (main branch)
- bandit
- docformatter
- python-safety-dependencies-check

To install the GitHub pre-commit hooks. This can be done in your virtual
environment by:
```shell
pre-commit install
```

## Testing
Use the following command (inside the app contaienr) to execute all tests using pytest:
```shell
pytest
```

### Debugging
You can debug your project using a debugger. When working with docker containers it's easier to use
a debugger called [WDB](https://github.com/Kozea/wdb). It allows to debug your workflow at runtime
using a web browser. You can debug tests or flows using the installed wdb debugger.
Don't worry, the docker-compose.yml file sets the necessary environment variables:
```shell
PYTHONBREAKPOINT: wdb.set_trace
WDB_SOCKET_SERVER: wdb
WDB_NO_BROWSER_AUTO_OPEN: 1
```

### How to use it
First, place a breakpoint:
```python
breakpoint()
```
The start the WDB container in the background:
```shell
docker compose up -d wdb
```

After that run your piece of code and check the statement inside the interactive console on: http://127.0.0.1:1984/
