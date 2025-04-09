# Flask API 

FROM python:3.11-alpine

RUN apk add --no-cache python3 py3-pip py3-virtualenv openssh
COPY requirements.txt api/requirements.txt

ARG IS_DEV
ENV IS_DEV=$IS_DEV

ARG HTTP
ENV HTTP=$HTTP

ARG API_HOST
ENV API_HOST=$API_HOST

ARG API_BASEPATH
ENV API_BASEPATH=$API_BASEPATH

ARG API_PORT
ENV API_PORT=$API_PORT

ARG API_ADMIN_USERNAME
ENV API_ADMIN_USERNAME=$API_ADMIN_USERNAME

ARG VIRTUOSO_HOST
ENV VIRTUOSO_HOST=$VIRTUOSO_HOST

ARG VIRTUOSO_PORT
ENV VIRTUOSO_PORT=$VIRTUOSO_PORT

RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN pip install -r api/requirements.txt

WORKDIR /api/src

CMD ["flask", "run", "--host=0.0.0.0"]
