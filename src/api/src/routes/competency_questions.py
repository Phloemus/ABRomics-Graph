
## Competency question routes
##
## All the routes that respond to prewritten competency questions. 
## A competency question is a question of interest that has been asked for by a biologist
##
## routes:
##

from flask_cors import cross_origin
from flask import jsonify

## Config imports
from config.config import *
from config.constants import *

## Util imports
from utils.query import Query


## List of the competency question queries
@cross_origin()
@app.route(f"/{API_BASEPATH}/query/competency-question", methods=['GET'])
def listCompetencyQuestions():
    response = COMPETENCY_QUESTION_QUERIES
    for query in response:
        with open(query['queryFilePath'], 'r') as file:
            queryContent = file.read()
        query["content"] = queryContent 
    return jsonify(response)


## Routes for the responses to the competency questions
@cross_origin()
@app.route(f"/{API_BASEPATH}/query/competency-question/<int:queryId>", methods=["GET"])
def getCompetencyQuestionResult(queryId):
    query = Query.fromFile(COMPETENCY_QUESTION_QUERIES[queryId-1]["queryFilePath"], SPARQL_ENDPOINT)

    response = jsonify(query.executeQuery())
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

