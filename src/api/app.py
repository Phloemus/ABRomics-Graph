
import sys 
import os
from flask import Flask, jsonify, request
from SPARQLWrapper import SPARQLWrapper, JSON

## Module imports
import modules.graph_creator


app = Flask(__name__)


API_ENDPOINT = f"{os.environ['HTTP']}{os.environ['API_HOST']}:{os.environ['API_PORT']}"
SPARQL_ENDPOINT = f"{os.environ['HTTP']}{os.environ['VIRTUOSO_HOST']}:{os.environ['VIRTUOSO_PORT']}/sparql"


QUERIES = [
    {
        "name": "count-nodes",
        "route": f"{API_ENDPOINT}/node/count",
        "method": "GET",
        "filePath": "queries/count-nodes-for-all-graphs.sparql",
        "description": """
            Return the number of nodes for each graphs present in the virtuoso server. 
        """,
        "parameters": {}
    },
    {
        "name": "count-samples-by-people",
        "route": f"{API_ENDPOINT}/sample/count/people",
        "method": "GET",
        "filePath": "queries/count-samples-by-people.sparql",
        "description": """
            Return the count of the samples for every person that uploded some in the abromics kg
        """,
        "parameters": {}
    },
    {
        "name": "count-samples-by-countries",
        "route": f"{API_ENDPOINT}/sample/count/countries",
        "method": "GET",
        "filePath": "queries/count-samples-by-countries.sparql",
        "description": """
            Return the count of the samples by countries that uploded some in the abromics kg
        """,
        "parameters": {}
    },
    {
        "name": "get-organs-for-specie",
        "route": f"{API_ENDPOINT}/organ",
        "method": "POST",
        "filePath": "queries/get-organs-by-specie-name.sparql",
        "description": """
            Get all the organs for a specific specie indicated by a specie_name
        """,
        "parameters": {
            "specie_name": "the name of the selected specie. Should be the latin name of the specie"
        }
    },
    {
        "name": "get-ktop-antibiotic-res-genes",
        "route": f"{API_ENDPOINT}/res-genes/best",
        "method": "GET",
        "filePath": "queries/q1-search-antibiotic-res-genes-all-sample.sparql",
        "description": """
            Get all the best antibiotic resistance genes for a given metric for all the samples
        """,
        "parameters": {
            "metric": "the label of the feature of interest that the antibiotic resistance genes should be filtered by"
        }
    }
]



## Util functions 
## 
## parameters: list of dictionnary {"string_to_replace": "defaultValue", "values": ["parameterA", "parameterB"]}
## 
def executeQuery(sparqlEndpointUrl, queryFilePath, parameters=[]):
    with open(queryFilePath, 'r') as file:
        query = file.read()

    for parameter in parameters:
        values = ""
        for value in parameter["values"]:
            values += f"{value}"
        query = query.replace(parameter["string_to_replace"], values) 
        print(query)

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
@app.route("/api")
def home():
    return jsonify({
        "version": "0.0.1",
        "message": "Welcome to ABRomics-kg API"
    })


## Routes that allow to modify the graph
@app.route("/api/build-graph", methods=['GET'])
def buildGraph():
    gc = GraphCreator()
    return jsonify({"message": "test 1 passed"})


## Routes that trigger SPARQL queries 
@app.route("/api/query", methods=['GET'])
def listAvailableQueries():
    return jsonify(QUERIES)

@app.route("/api/node/count", methods=[QUERIES[0]["method"]])
def countNodesInAllGraphs():
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[0]["filePath"]))

@app.route("/api/sample/count/people", methods=[QUERIES[1]["method"]])
def countSamplesInGraphByPeople():
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[1]["filePath"]))

@app.route("/api/sample/count/countries", methods=[QUERIES[2]["method"]])
def countSamplesInGraphByCountries():
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[2]["filePath"]))

@app.route("/api/organ", methods=[QUERIES[3]["method"]])
def listAvailableOrgansForSpecieName():
    specieName = request.json["specie_name"]
    query_parameters = [ {"string_to_replace": "Homo sapiens", "values": [specieName]} ]
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[3]["filePath"], query_parameters))


## Compentency questions
@app.route("/api/get-ktop-antibiotic-res-genes", methods=[QUERIES[4]["method"]])
def getKTopAntibioticResGenes():
    metric = request.json["metric"]
    query_parameters = [ {"string_to_replace": "Gene Length", "values": [metric]} ]
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[4]["filePath"]))




## Launch the Flask app (the ABRomics-KG API)
if __name__ == '__main__':
    app.run(host=os.environ['API_HOST'], port=os.environ['API_PORT'], debug=True)
