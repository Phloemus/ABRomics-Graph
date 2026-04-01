
## Competency question routes
##
## All the routes that respond to prewritten competency questions. 
## A competency question is a question of interest that has been asked for by a biologist
##
## routes:
##


from flask_cors import CORS, cross_origin
from flask import jsonify, request

## Config imports
from config.config import *
from config.constants import *

## Util imports
from utils.query import Query


## Out dated
#@cross_origin()
#@app.route(f"/{API_BASEPATH}/organ", methods=[QUERIES[3]["method"]])
#def listAvailableOrgansForSpecieName():
#    specieName = request.json["specie_name"]
#    query_parameters = [ {"string_to_replace": "Homo sapiens", "values": [specieName]} ]
#    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[3]["filePath"], query_parameters))

## Compentency questions
@cross_origin()
@app.route(f"/{API_BASEPATH}/res-genes/best", methods=[QUERIES[4]["method"]])
def getKTopAntibioticResGenes():
    query = Query.fromFile(QUERIES[4]["filePath"], SPARQL_ENDPOINT)

    response = jsonify(query.executeQuery())
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

