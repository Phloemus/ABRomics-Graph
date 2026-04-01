
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
        "routes": [
            {
                "name": "List all queries",
                "description": "List all the prewritten SPARQL queries that can be accessed through the API ",
                "url": f"{API_ENDPOINT}/{API_BASEPATH}/query",
                "method": "GET"
            },
            {
                "name": "List all stat queries",
                "description": "List all the queries that give stats on the KG and its content",
                "url": f"{API_ENDPOINT}/{API_BASEPATH}/query/stat",
                "method": "GET"
            },
            {
                "name": "List all competency question queries",
                "description": "List all the queries used as relevant biological questions of interest which were used to assess the KG relevancy",
                "url": f"{API_ENDPOINT}/{API_BASEPATH}/query/competency-question",
                "method": "GET"
            },
            {
                "name": "Execute a custom query",
                "description": "Used to perform a custom SPARQL query written by a user on the KG",
                "url": f"{API_ENDPOINT}/{API_BASEPATH}/query/custom",
                "method": "POST",
                "body": "{'query': <sparql_query_as_string>}",
                "bodyType": "json"
            }
        ]
    })

## Route that is used to list the queries routes
@cross_origin()
@app.route(f"/{API_BASEPATH}/query", methods=['GET'])
def listAvailableQueries():
    return jsonify({
        "stat": "",
        "competency-questions": COMPETENCY_QUESTION_QUERIES,
        "other": QUERIES
    })

