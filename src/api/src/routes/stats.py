
## Statistics routes
##
## All the routes that are related to getting statistics on the 
## knowledge graph such as the number of nodes etc
##
## routes:
## - [GET] countNodesInAllGraphs: Get the number of nodes in every named graph in the virtuoso 
##                                graph server
## - [GET] countSamplesInGraphByPeople: Get the number of samples every person has uploaded to
##                                      the ABRomics platform
## - [GET] countSamplesInGraphByCountries: Get the number of samples for every country 
##


from flask_cors import CORS, cross_origin
from flask import jsonify

## Config imports
from config.config import *
from config.constants import *

## Util imports
from utils.authentification import *
from utils.query import Query


@cross_origin()
@app.route(f"/{API_BASEPATH}/node/count", methods=[QUERIES[0]["method"]])
def countNodesInAllGraphs():
    query = Query(QUERIES[0]["filePath"], sparqlEndpoint=SPARQL_ENDPOINT)
    return jsonify(query.executeQuery())

@cross_origin()
@app.route(f"/{API_BASEPATH}/sample/count/people", methods=[QUERIES[1]["method"]])
def countSamplesInGraphByPeople():
    query = Query(QUERIES[1]["filePath"], sparqlEndpoint=SPARQL_ENDPOINT)
    return jsonify(query.executeQuery())

@cross_origin()
@app.route(f"/{API_BASEPATH}/sample/count/countries", methods=[QUERIES[2]["method"]])
def countSamplesInGraphByCountries():
    query = Query(QUERIES[2]["filePath"], sparqlEndpoint=SPARQL_ENDPOINT)
    return jsonify(query.executeQuery())

