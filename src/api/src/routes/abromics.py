
## ABRomics api routes
##
## The routes of the API that are used by the abromics platform
##
## routes:
## - [GET] 
## 


from flask_cors import CORS, cross_origin
from flask_caching import Cache
from flask import jsonify, request

## Config imports
from config.config import *
from config.constants import *


## Module imports
from utils.query import Query


@cross_origin()
@app.route(f"/{API_BASEPATH}/sample-sources", methods=[QUERIES[5]["method"]])
def getSampleSources():
    specieName = ""
    sampleType = ""

    if "specieName" in request.json:
        specieName = request.json["specieName"]
    if "sampleType" in request.json:
        sampleType = request.json["sampleType"]

    if sampleType == "human":
        query = Query(QUERIES[5]["filePath"]["animal"], sparqlEndpoint=SPARQL_ENDPOINT, parameters={"specieName": "Homo sapiens" })
    elif sampleType == "animal":
        if specieName == "":
            query = Query(QUERIES[5]["filePath"]["animal-no-specie"], sparqlEndpoint=SPARQL_ENDPOINT) ## Only animal no specific specie
        else:
            query = Query(QUERIES[5]["filePath"]["animal"], sparqlEndpoint=SPARQL_ENDPOINT, parameters={"specieName": specieName })
    elif sampleType == "environmental":
        query = Query(QUERIES[5]["filePath"]["environmental"], sparqlEndpoint=SPARQL_ENDPOINT) ## Only environmental
    else:
        query = Query(QUERIES[5]["filePath"]["all"], sparqlEndpoint=SPARQL_ENDPOINT) ## All sample sources all species 

    return jsonify(query.executeQuery())


#### Takes too much time, implement some caching mecanisms here ####

@cross_origin()
@cache.cached(timeout=50)
@app.route(f"/{API_BASEPATH}/microorganisms")
def getMicroorgnismSpecies():
    query = Query(QUERIES[6]["filePath"], sparqlEndpoint=SPARQL_ENDPOINT) ## All the bacteria species name
    ## query.exportQueryResult("cache/microorganisms/test.json") ## test for the cache feature
    return jsonify(query.executeQuery())


@cross_origin()
@app.route(f"/{API_BASEPATH}/hosts")
def getHostSpecies():
    query = Query(QUERIES[7]["filePath"], sparqlEndpoint=SPARQL_ENDPOINT) ## All the host species name
    return jsonify(query.executeQuery())
