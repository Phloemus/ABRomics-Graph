
from flask import Flask, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON


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
        "name": "count-samples",
        "method": "GET",
        "filePath": "queries/count-samples-by-person.sparql",
        "description": """
            Return count the samples for every people that uploded some in the abromics kg
        """,
        "parameters": {}
    }
]

SPARQL_ENDPOINT = "http://localhost:8890/sparql"


## Util functions 
def executeQuery(sparqlEndpointUrl, queryFilePath, Parameters={}):
    with open(queryFilePath, 'r') as file:
        query = file.read()
     
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


## Routes that trigger SPARQL queries 
@app.route("/query", methods=['GET'])
def listAvailableQueries():
    return jsonify(QUERIES)

@app.route("/node/count", methods=[QUERIES[0]["method"]])
def countNodesInAllGraphs():
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[0]["filePath"]))

@app.route("/sample/count", methods=[QUERIES[1]["method"]])
def countSamplesInGraph():
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[1]["filePath"]))



## Launch the Flask app (the ABRomics-KG API)
if __name__ == '__main__':
    app.run(debug=True)
