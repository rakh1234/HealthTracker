FROM python:3.9-alpine3.13  
LABEL maintainer="Healthtracker.com"  

ENV PYTHONUNBUFFERED 1  

WORKDIR /app
COPY . /app/

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /app/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /app/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"  
ENV PYTHONPATH=/app

RUN chown -R django-user:django-user /app
USER django-user

EXPOSE 8000