# Use Python 3.13 as the base image
FROM python:3.13-slim AS base

# Set the working directory in the container
WORKDIR /app

# Install dependencies required for Poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry version 2.1.1
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set environment variables for Poetry
ENV POETRY_VERSION=2.1.1
ENV PATH="/root/.local/bin:${PATH}"

# Copy the poetry.lock and pyproject.toml files to install dependencies
# Copy poetry configuration files first to install dependencies
COPY pyproject.toml poetry.lock /app/

# Install the dependencies using Poetry
RUN poetry install --no-interaction --no-root

# Copy the rest of your application code into the container
COPY . /app/

# Expose port 8080
EXPOSE 8080

# Command to run Uvicorn server
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
