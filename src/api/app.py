
from flask import Flask, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON


app = Flask(__name__)

queries = [
    {
        "name": "count-all",
        "method": "GET",
        "filePath": "queries/count-nodes-for-all-graphs.sparql",
        "description": """
            Return the number of nodes for each graphs present in the virtuoso server. 
        """,
        "parameters": {}
    }
]

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




@app.route("/")
def home():
    return jsonify({
        "version": "0.0.1",
        "message": "Welcome to ABRomics-kg API"
    })


@app.route("/query", methods=['GET'])
def listAvailableQueries():
    return jsonify(queries)

@app.route("/query/count-all", methods=[queries[0]["method"]])
def countNodesInAllGraphs():
    return jsonify(executeQuery("http://localhost:8890/sparql", queries[0]["filePath"]))



if __name__ == '__main__':
    app.run(debug=True)
