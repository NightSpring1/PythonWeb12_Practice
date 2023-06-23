# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the working directory
COPY . /app

# Install Poetry
RUN pip install poetry

# Install project dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi


EXPOSE 80
# Set the entrypoint to run the main.py script
ENTRYPOINT ["python", "main.py"]
