
## Configuration file
##
## Load all the environment variable needed for the API to work properly
## depending on the type of environment is used as well as the flask app configuration


import os
from flask import Flask
from flask_cors import CORS


if "IS_DEV" in os.environ and os.environ['IS_DEV'] == "false":
    API_PORT = f"{os.environ['API_PORT']}"
    API_ENDPOINT = f"{os.environ['HTTP']}{os.environ['API_HOST']}:{os.environ['API_PORT']}"
    API_BASEPATH = f"{os.environ['API_BASEPATH']}"
    SPARQL_ENDPOINT = f"{os.environ['VIRTUOSO_HOST']}:{os.environ['VIRTUOSO_PORT']}/sparql"
    ADMIN_USERNAME = f"{os.environ['API_ADMIN_USERNAME']}"
    ADMIN_PASSWORD = f"{os.environ['API_ADMIN_PASSWORD']}"
else:   
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

cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

