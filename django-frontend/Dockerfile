FROM python:3.12-alpine3.18

# Set the environment variable
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

# Set the working directory
WORKDIR /app

COPY requirements.txt .
COPY src .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "entrypoint.sh"]