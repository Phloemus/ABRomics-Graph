
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

## List of the competency question queries
@cross_origin()
@app.route(f"/{API_BASEPATH}/query/competency-question", methods=['GET'])
def listCompetencyQuestions():
    for query in COMPETENCY_QUESTION_QUERIES:
        with open(query.queryFilePath, 'r') as file:
            queryContent = file.read()
        ##! Add the query content for all competency questions queries in the response
    return jsonify(COMPETENCY_QUESTION_QUERIES)


## Compentency questions 1
@cross_origin()
@app.route(f"/{API_BASEPATH}/res-genes/best", methods=[QUERIES[4]["method"]])
def getKTopAntibioticResGenes():
    query = Query.fromFile(QUERIES[4]["filePath"], SPARQL_ENDPOINT)

    response = jsonify(query.executeQuery())
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

