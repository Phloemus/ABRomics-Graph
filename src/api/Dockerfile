# Flask API 

FROM python:3.11-alpine

RUN apk add --no-cache python3 py3-pip py3-virtualenv
COPY requirements.txt api/requirements.txt
COPY app.py api/app.py
COPY modules api/modules
COPY data api/data
COPY queries api/queries

RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN pip install -r api/requirements.txt

WORKDIR /api

CMD ["python3", "app.py"]
