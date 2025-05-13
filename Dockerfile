FROM python:3.13-slim AS base

WORKDIR /app

# Install system dependencies for building packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=2.1.1 python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

ENV PATH="/root/.local/bin:${PATH}"

# Copy only poetry files to leverage Docker cache
COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-interaction --no-root --without dev

# Now copy the rest of the app
COPY . /app/

EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]