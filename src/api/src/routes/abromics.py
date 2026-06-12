
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
    specieName = request.args.get('specieName')
    sampleType = request.args.get('sampleType')
    
    if sampleType == "human":
        query = Query.fromFile(QUERIES[5]["filePath"]["animal"], sparqlEndpoint=SPARQL_ENDPOINT, parameters={"specieName": "Homo sapiens" })
    elif sampleType == "animal":
        if specieName == "":
            query = Query.fromFile(QUERIES[5]["filePath"]["animal-no-specie"], sparqlEndpoint=SPARQL_ENDPOINT) ## Only animal no specific specie
        else:
            query = Query.fromFile(QUERIES[5]["filePath"]["animal"], sparqlEndpoint=SPARQL_ENDPOINT, parameters={"specieName": specieName })
    elif sampleType == "environmental":
        query = Query.fromFile(QUERIES[5]["filePath"]["environmental"], sparqlEndpoint=SPARQL_ENDPOINT) ## Only environmental
    else:
        query = Query.fromFile(QUERIES[5]["filePath"]["all"], sparqlEndpoint=SPARQL_ENDPOINT) ## All sample sources all species 

    response = jsonify(query.executeQuery())
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response


@cross_origin()
@app.route(f"/{API_BASEPATH}/sample-sources/popular", methods=[QUERIES[8]["method"]])
def getPopularSampleSources():
    query = Query.fromFile(QUERIES[8]["filePath"], sparqlEndpoint=SPARQL_ENDPOINT)
    response = jsonify(query.executeQuery())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


#### Takes too much time, implement some caching mecanisms here ####

@cross_origin()
@cache.cached(timeout=50) ## 
@app.route(f"/{API_BASEPATH}/microorganisms")
def getMicroorgnismSpecies():
    query = Query.fromFile(QUERIES[6]["filePath"], sparqlEndpoint=SPARQL_ENDPOINT) ## All the bacteria species name
    query.exportQueryResult("cache/microorganisms/test.json") ## test for the cache feature 
    response = jsonify(query.executeQuery())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@cross_origin()
@app.route(f"/{API_BASEPATH}/hosts")
def getHostSpecies():
    query = Query.fromFile(QUERIES[7]["filePath"], sparqlEndpoint=SPARQL_ENDPOINT) ## All the host species name
    response = jsonify(query.executeQuery())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@cross_origin()
@app.route(f"/{API_BASEPATH}/resistance-genes/aro-class", methods=[QUERIES[9]["method"]])
def getResistanceGenesAROClasses():
    resistanceGenesList = request.json["resistanceGenes"]
    resistanceGenesString = ""
    for resistanceGeneName in resistanceGenesList:
        resistanceGenesString += f"'{resistanceGeneName}' "
    query = Query.fromFile(
        QUERIES[9]["filePath"], 
        sparqlEndpoint=SPARQL_ENDPOINT, 
        parameters={"resistanceGenes": resistanceGenesString}
    ) ## Get the aro classes of a list of resistance genes
    rawResponse = query.executeQuery()
    rawResponse = {item["resistanceGene"]["value"]: item["aroClass"]["value"] for item in rawResponse}
    response = jsonify(rawResponse)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response