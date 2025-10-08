
## Configuration file
##
## Load all the environment variable needed for the API to work properly
## depending on the type of environment is used as well as the flask app configuration


import os
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache


if "IS_DEV" in os.environ and os.environ['IS_DEV'] == "false": ##? IS_DEV might be at fault here ..  
    print("waaaawww")
    API_PORT = f"{os.environ['API_PORT']}"
    API_ENDPOINT = f"{os.environ['HTTP']}{os.environ['API_HOST']}:{os.environ['API_PORT']}"
    API_BASEPATH = f"{os.environ['API_BASEPATH']}"
    SPARQL_ENDPOINT = f"{os.environ['VIRTUOSO_HOST']}/sparql"
    ADMIN_USERNAME = f"{os.environ['API_ADMIN_USERNAME']}"
    ADMIN_PASSWORD = f"{os.environ['API_ADMIN_PASSWORD']}"
else:    
    print("ahhh expected..")
    API_PORT = "5000"
    API_ENDPOINT = "http://localhost:5000"
    API_BASEPATH = f"graph-api"
    SPARQL_ENDPOINT = "http://localhost:8890/sparql"
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin"

CACHE_DIR="cache"
QUERY_DIR="queries"


## API configuration
app = Flask(__name__)
app.config['secret_key'] = "this is secret"

config = {
    "DEBUG": True,          
    "CACHE_TYPE": "SimpleCache",  
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CORS_HEADERS": 'Content-Type'
}

app.config.from_mapping(config)
## cors = CORS(app) 
cache = Cache(app)

