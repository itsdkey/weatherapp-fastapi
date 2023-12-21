# Weather app using FastAPI

* [Intuition](#intuition)
* [Local development](#local-development-using-virtualenv)
    * [using virtualenv](#local-development-using-virtualenv)
    * [using docker compose](#local-development-using-docker-compose)
* [Project conventions](#project-conventions)

## Intuition
Just a fun project to code a simple weather app. However, I wanted to get familair with new technologies such as:
- [FastAPI](https://fastapi.tiangolo.com/)
- [InfluxDB](https://www.influxdata.com/)


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