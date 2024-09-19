# Dockerfile for /dev/api built with FastAPI
# Complete this file to match the content require for fastAPI to work 

FROM python:3.9

COPY requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY . /api

WORKDIR /api

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
