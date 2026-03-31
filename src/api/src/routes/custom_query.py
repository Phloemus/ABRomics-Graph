

## Custom query api routes
##
## The api routes associated with the execution of custom queries send by the end user
## These routes will be queries within the main app or accessed by external users
##
## routes:
## - [GET] customQuery: Return the querie's raw response from the graph server 
## 


from flask_cors import CORS, cross_origin
from flask import jsonify, request, make_response

## Config imports
from config.config import *
from config.constants import *


## Custom query route
@cross_origin()
@app.route(f"/{API_BASEPATH}/query/custom", methods=["POST"])
def customQuery():

    queryContent = request.json["query"]
    query = Query(queryContent, SPARQL_ENDPOINT)

    response = jsonify(query.executeQuery())
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
