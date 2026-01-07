
## Basic api routes
##
## The basic api routes are routes that are used to get the very basic informations about the 
## API, such as its version and the queries that can be performed using the API
##
## routes:
## - [GET] home: gives the version of the ABRomics Graph API as well as the a welcome message
## - [GET] listAvailableQueries: return list with all the queries and descriptions available by the API
## 


from flask_cors import CORS, cross_origin
from flask import jsonify

## Config imports
from config.config import *
from config.constants import *


## Home Route
@cross_origin()
@app.route(f"/{API_BASEPATH}")
def home():
    return jsonify({
        "version": "0.0.1",
        "message": "Welcome to ABRomics-kg API",
        "routes": f"{API_ENDPOINT}/{API_BASEPATH}/query"
    })


## Routes that trigger SPARQL queries 
@cross_origin()
@app.route(f"/{API_BASEPATH}/query", methods=['GET'])
def listAvailableQueries():
    return jsonify(QUERIES)

