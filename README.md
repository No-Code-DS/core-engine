![Linters](https://github.com/No-Code-DS/core-engine/actions/workflows/tox.yml/badge.svg)
![Deployment](https://github.com/No-Code-DS/core-engine/actions/workflows/docker-deploy.yml/badge.svg?branch=main)

# core-engine

Main service of **Data Lume** no-code data science platform responsible for data cleaning, feature engineering and model deployment implemented in FastAPI.

## Run locally

First Clone the project

```sh
# clone the repo
git clone https://github.com/No-Code-DS/core-engine.git


# install requirements
cd engine
pip install -r requirements.txt
# or
pip install .
```

Prepare postgresql database

```sh
# set environment variable with connection string
export SQLALCHEMY_DATABASE_URL="postgresql://{user}:{password}@db/{dbname}"

# apply migrations
alembic upgrade head 
```

Start the application with:
```sh
uvicorn engine.main:app --host 0.0.0.0 --port 8000 --reload
```
