# Use Python 3.13 slim image as the base image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install Poetry (2024 version, stable release)
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to the PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject.toml and poetry.lock if present
COPY pyproject.toml poetry.lock* /app/

# Install dependencies with Poetry
RUN poetry install --no-interaction --no-dev

# Copy the rest of the application code into the container
COPY . /app/

# Expose port 80
EXPOSE 80

# Run FastAPI using Poetry and Uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "80"]