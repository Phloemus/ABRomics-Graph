# Dockerfile for /dev/api built with FastAPI
# Complete this file to match the content require for fastAPI to work 

FROM python:3.9

COPY requirements.txt api/requirements.txt
COPY app.py api/app.py
COPY modules api/modules
COPY modules api/queries
COPY data api/data

WORKDIR /api

RUN python3 -m pip install -r requirements.txt

EXPOSE 5000

CMD ["uwsgi", "--http", "127.0.0.1:5000", "--master", "-p", "4", "-w", "app.py"]
