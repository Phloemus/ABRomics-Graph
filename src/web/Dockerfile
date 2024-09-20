FROM python:3.9-slim

WORKDIR /streamlit/app

COPY app /streamlit/app

RUN apt-get update && apt-get install -y 

RUN pip3 install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
