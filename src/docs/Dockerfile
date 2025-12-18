FROM python:3.11-alpine

RUN apk add --no-cache python3 py3-pip py3-virtualenv
COPY requirements.txt requirements.txt
COPY mkdocs.yaml mkdocs.yaml
COPY schema.yaml schema.yaml
COPY entrypoint.sh entrypoint.sh

RUN chmod +x entrypoint.sh

RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "entrypoint.sh"]
