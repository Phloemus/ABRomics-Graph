# Dockerfile for /dev/api built with FastAPI
# Complete this file to match the content require for fastAPI to work 

FROM python:3.9

COPY requirements.txt api/requirements.txt
COPY app.py api/app.py
COPY modules api/modules
COPY modules api/queries
COPY data api/data

RUN python3 -m pip install -r requirements.txt

WORKDIR /api

EXPOSE 8080

CMD ["uwsgi", "--http", "127.0.0.1:8080", "--master", "-p", "4", "-w", "app:app"]
