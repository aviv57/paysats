# Use an official Python runtime as a parent image
FROM python:3.13

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
# Add poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy the poetry configuration and lock files
COPY pyproject.toml poetry.lock /app/

# Install dependencies with Poetry
RUN poetry install --no-interaction --no-dev

# Copy the rest of the application code into the container
COPY . /app/

# Specify the command to run your app
CMD ["poetry", "run", "python", "your_app.py"]
