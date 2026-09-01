FROM python:3.11-slim

ENV POETRY_VERSION=1.8.4 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY pyproject.toml README.md ./
COPY equalexperts_dataeng_exercise ./equalexperts_dataeng_exercise

RUN poetry install --only main

ENTRYPOINT ["poetry", "run", "exercise"]
