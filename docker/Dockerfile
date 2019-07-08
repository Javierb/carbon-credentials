FROM python:3.7.3-alpine
ENV PYTHONUNBUFFERED 1
LABEL Name=carbon-credentials

COPY ./requirements /requirements

RUN apk update \
    && apk add --no-cache --virtual .build-deps build-base linux-headers gcc musl-dev \
    # Install common dependencies (psycopg2)
    && apk add --no-cache postgresql-dev \
    && pip install --upgrade pip \
    # Translations dependencies
    # && apk add gettext \
    && pip install --no-cache-dir -r /requirements/dev.txt \
    # Remove un-needed build libraries
    && apk del .build-deps

COPY ./docker/wait-for.sh /wait-for.sh
COPY ./docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /wait-for.sh /entrypoint.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
