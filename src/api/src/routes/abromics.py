
## ABRomics api routes
##
## The routes of the API that are used by the abromics platform
##
## routes:
## - [GET] 
## 


from flask_cors import CORS, cross_origin
from flask import jsonify, request

## Config imports
from config.config import *
from config.constants import *


## Module imports
from utils.query import Query


@cross_origin()
@app.route(f"/{API_BASEPATH}/sample-sources", methods=[QUERIES[5]["method"]])
def getSampleSources():
    specieName = request.json["specieName"]
    query = Query(QUERIES[5]["filePath"], sparqlEndpoint=SPARQL_ENDPOINT, parameters={"specieName": specieName})
    return jsonify(query.executeQuery())

