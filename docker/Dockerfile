FROM python:3.12.7-slim-bullseye

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.2

WORKDIR /app/quoteGen

COPY pyproject.toml poetry.lock /app/quoteGen/

RUN poetry config virtualenvs.create false
RUN poetry install --only main
RUN apt-get purge -y && rm -rf /var/lib/apt/lists/*

COPY . /app/quoteGen/