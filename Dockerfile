# Base image
FROM python:3.13 as python-base

# Set environment variables
ENV POETRY_VERSION=2.1.2 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Create working directory
WORKDIR /app

# Copy only requirements to cache dependencies
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application
COPY . /app

# Expose port
EXPOSE 8081

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8081"]
