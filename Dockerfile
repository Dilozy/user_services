FROM python:3.12.11-alpine3.22

WORKDIR /application

RUN pip install poetry

COPY poetry.lock pyproject.toml /application/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY user_services /application/user_services

COPY bot /application/bot

RUN adduser --disabled-password app-admin

USER app-admin

EXPOSE 8000