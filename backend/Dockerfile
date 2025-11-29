FROM python:3.10.12-slim-buster AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    WORKDIR=/usr/src/app

WORKDIR $WORKDIR

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --upgrade pip && pip install poetry
RUN poetry config installer.max-workers 10
RUN poetry config virtualenvs.in-project true
COPY pyproject.toml ./
RUN poetry install --only main --no-root && rm -rf "$POETRY_CACHE_DIR"


FROM python:3.10.12-slim-buster AS base

ENV WORKDIR=/usr/src/app \
    PATH="/usr/src/app/.venv/bin:$PATH"

COPY --from=builder $WORKDIR $WORKDIR
WORKDIR $WORKDIR
ENV PYTHONPATH=$WORKDIR:$PYTHONPATH
COPY . .
RUN mkdir -p /static

CMD chmod +x ./wait-for-it.sh && \
    ./wait-for-it.sh redis:6379 && \
    ./wait-for-it.sh postgres:5432 && \
    alembic upgrade head && \
    python3 ./app/initial_data.py && \
    gunicorn -c ./app/core/dep_config.py app.main:app --forwarded-allow-ips '*' & \
    arq app.utils.worker.WorkerSettings
