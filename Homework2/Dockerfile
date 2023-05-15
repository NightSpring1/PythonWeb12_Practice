FROM python:3.10

LABEL authors="Alexander Singaevsky"

# Set the working directory in the container
WORKDIR /bot

# Install Pipenv
RUN pip install pipenv

# Copy package files to the container
COPY . /bot/package
# Install package into pipenv
RUN pipenv install /bot/package

# Set the entrypoint command for the container
CMD ["pipenv", "run", "bot-start"]