# Flask API 

FROM python:3.11-alpine

RUN apk add --no-cache python3 py3-pip py3-virtualenv
COPY requirements.txt api/requirements.txt
COPY modules api/modules
COPY data api/data
COPY queries api/queries

ARG HTTP
ENV HTTP=$HTTP

ARG API_HOST
ENV API_HOST=$API_HOST

ARG API_BASEPATH
ENV API_BASEPATH=$API_BASEPATH

ARG API_PORT
ENV API_PORT=$API_PORT

ARG FLASK_ENV
ENV FLASK_ENV=$FLASK_ENV

ARG VIRTUOSO_HOST
ENV VIRTUOSO_HOST=$VIRTUOSO_HOST

ARG VIRTUOSO_PORT
ENV VIRTUOSO_PORT=$VIRTUOSO_PORT

RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN pip install -r api/requirements.txt

WORKDIR /api

CMD ["flask", "run", "--host=0.0.0.0"]
