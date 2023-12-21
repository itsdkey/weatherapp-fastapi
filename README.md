# Weather app using FastAPI

* [Intuition](#intuition)
* [What I used](#what-i-used)
* [What patterns I followed](#what-patterns-i-followed)
* [Local development](#local-development-using-virtualenv)
    * [using virtualenv](#local-development-using-virtualenv)
    * [using docker compose](#local-development-using-docker-compose)
* [Project conventions](#project-conventions)

## Intuition
Just a fun project to code a simple weather app. However, I wanted to get more familiar
with new technologies such as:
- [FastAPI](https://fastapi.tiangolo.com/)
- [InfluxDB](https://www.influxdata.com/)


## What I used
To learn something about the technologies (follow some conventions mentioned in their
documentations) and also to follow best practices I used the following concepts:
- Use [env vars](https://fastapi.tiangolo.com/advanced/settings/#environment-variables)
for WeatherClient domain and API Key (so we can change and for security reasons),
- [Use FastAPI's Settings Object](https://fastapi.tiangolo.com/advanced/settings/#create-the-settings-object)


# What patterns I followed
To keep following the best practices and to have my code more structured I decided to follow the patterns below:
- A Client class for 3rd party integration - so the code responsible for requesting 3rd parties is separated from the rest
- [Adapter design pattern](https://refactoring.guru/design-patterns/adapter) - so I can convert the 3rd party response
the way I want it to be used by my app


## Local development using virtualenv
First, check which Python version is used in the Dockerfile.
If you do not have the current version please install it.
Then create a python virtual env:
```shell
python3.12 -m venv env/
```

Activate the env and set PYTHONPATH:
```shell
source env/bin/activate
export PYTHONPATH=`pwd`
```

Install the requirements:
```shell
pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt
```

Start the app by:
```shell
uvicorn main:app --reload
```

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