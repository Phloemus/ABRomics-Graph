
import sys
from flask import Flask, jsonify, request
from SPARQLWrapper import SPARQLWrapper, JSON

## Module imports
import modules.graph_creator


app = Flask(__name__)

## Constants
QUERIES = [
    {
        "name": "count-nodes",
        "method": "GET",
        "filePath": "queries/count-nodes-for-all-graphs.sparql",
        "description": """
            Return the number of nodes for each graphs present in the virtuoso server. 
        """,
        "parameters": {}
    },
    {
        "name": "count-samples-by-people",
        "method": "GET",
        "filePath": "queries/count-samples-by-people.sparql",
        "description": """
            Return count the samples for every person that uploded some in the abromics kg
        """,
        "parameters": {}
    },
    {
        "name": "count-samples-by-countries",
        "method": "GET",
        "filePath": "queries/count-samples-by-countries.sparql",
        "description": """
            Return count the samples by countries that uploded some in the abromics kg
        """,
        "parameters": {}
    },
    {
        "name": "get-organs-for-specie",
        "method": "POST",
        "filePath": "queries/get-organs-by-specie-name.sparql",
        "description": """
            Get all the organs for a specific specie indicated by a specie_name
        """,
        "parameters": {
            "specie_name": "the name of the selected specie. Should be the latin name of the specie"
        }
    }
]

SPARQL_ENDPOINT = "http://localhost:8890/sparql"


## Util functions 
## 
## parameters: list of dictionnary {"stringToReplace": "parameterValue"} (for one value)
## parameters: list of dictionnary {"stringToReplace": ["parameterValue1", "parameterValue2"]} (for multiple values to change)
## (this doesn't work for the queries where there are multiple values that should be changed)
## 
def executeQuery(sparqlEndpointUrl, queryFilePath, parameters=[]):
    with open(queryFilePath, 'r') as file:
        query = file.read()

    for parameter in parameters:
        print(parameter)
        ## modify the query accordingly to the parameter

    sparql = SPARQLWrapper(sparqlEndpointUrl)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    try:
        res = sparql.query().convert()
        recs = res["results"]["bindings"]
        return recs
    except Exception as e:
        print(e)
        return {"status": "error", "message": str(e)}



## Home Route
@app.route("/")
def home():
    return jsonify({
        "version": "0.0.1",
        "message": "Welcome to ABRomics-kg API"
    })


## Routes that allow to modify the graph
@app.route("/build-graph", methods=['GET'])
def buildGraph():
    gc = GraphCreator()
    return jsonify({"message": "test 1 passed"})


## Routes that trigger SPARQL queries 
@app.route("/query", methods=['GET'])
def listAvailableQueries():
    return jsonify(QUERIES)

@app.route("/node/count", methods=[QUERIES[0]["method"]])
def countNodesInAllGraphs():
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[0]["filePath"]))

@app.route("/sample/count/people", methods=[QUERIES[1]["method"]])
def countSamplesInGraphByPeople():
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[1]["filePath"]))

@app.route("/sample/count/countries", methods=[QUERIES[2]["method"]])
def countSamplesInGraphByCountries():
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[2]["filePath"]))

@app.route("/organ", methods=[QUERIES[3]["method"]])
def listAvailableOrgansForSpecieName():
    specieName = request.json["specie_name"]
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[3]["filePath"]))




## Launch the Flask app (the ABRomics-KG API)
if __name__ == '__main__':
    app.run(debug=True)
