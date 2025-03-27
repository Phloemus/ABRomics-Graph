
import sys 
import os
import jwt
import datetime
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from SPARQLWrapper import SPARQLWrapper, JSON

## Module imports
import modules.graph_creator


## API configuration
app = Flask(__name__)
app.config['secret_key'] = "this is secret"

cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'


## Fetching the environment variables depending on the is_dev flag
if "IS_DEV" in os.environ and os.environ['IS_DEV'] == "false":
    API_PORT = f"{os.environ['API_PORT']}"
    API_ENDPOINT = f"{os.environ['HTTP']}{os.environ['API_HOST']}:{os.environ['API_PORT']}"
    API_BASEPATH = f"{os.environ['API_BASEPATH']}"
    SPARQL_ENDPOINT = f"{os.environ['HTTP']}{os.environ['VIRTUOSO_HOST']}:{os.environ['VIRTUOSO_PORT']}/sparql"
    ADMIN_USERNAME = f"{os.environ['API_ADMIN_USERNAME']}"
    ADMIN_PASSWORD = f"{os.environ['API_ADMIN_PASSWORD']}"
else:   
    API_PORT = "5000"
    API_ENDPOINT = "http://localhost:5000"
    API_BASEPATH = f"graph-api"
    SPARQL_ENDPOINT = "http://localhost:8890/sparql"
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin"


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

ADMIN_QUERIES = [
    {
        "name": "delete-all-nodes",
        "route": f"{API_ENDPOINT}/graph",
        "method": "DELETE",
        "filePath": "queries/delete-all-nodes.sparql",
        "description": """
            Delete all the nodes present in the knowledge graph 
        """
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
        return {"status": "error", "message": str(e), "endpoint": SPARQL_ENDPOINT}


## Middleware functions
## 
def authentification_required(f):
    def decorated(*args, **kwargs):
        token = request.json['token']
        if not token:
            return jsonify({'error': 'token is missing'}), 403
        try:
            jwt.decode(token, app.config['secret_key'], algorithms="HS256")
        except Exception as error:
            return jsonify({'error': 'token is invalid/expired'})
        return f(*args, **kwargs)
    return decorated


## API routes functions
##
##
##


## Home Route
@cross_origin()
@app.route(f"/{API_BASEPATH}")
def home():
    return jsonify({
        "version": "0.0.1",
        "message": "Welcome to ABRomics-kg API"
    })


## Login route
@app.route(f"/{API_BASEPATH}/login", methods=['POST'])
def login():
    username = request.json["username"]
    password = request.json["password"]
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3)}, app.config['secret_key'])
        return jsonify({"token": token})
    else:
        return make_response(jsonify({"message": "wrong username or password"}), 401)


## protected test route
## Use this function in development to test if you have access to the protected routes of the API
@app.route(f"/{API_BASEPATH}/protected", methods=['POST'])
@authentification_required
def protected():
    return jsonify({"message": "protected route tested"})


## Route that delete all the content (all the nodes) of the knowledge graph
@app.route(f"/{API_BASEPATH}/graph", methods=['DELETE'])
@authentification_required
def deleteGraphData():
    executeQuery(ADMIN_QUERIES[0]["filePath"])
    return jsonify({"message": "graph delete successfully"})


## Routes that allow to modify the graph
## Check if this route works and protect it behind authentification 
@cross_origin()
@app.route(f"/{API_BASEPATH}/build-graph", methods=['GET'])
def buildGraph():
    gc = GraphCreator()
    return jsonify({"message": "test 1 passed"})


## Routes that trigger SPARQL queries 
@cross_origin()
@app.route(f"/{API_BASEPATH}/query", methods=['GET'])
def listAvailableQueries():
    return jsonify(QUERIES)

@cross_origin()
@app.route(f"/{API_BASEPATH}/node/count", methods=[QUERIES[0]["method"]])
def countNodesInAllGraphs():
    print(QUERIES[0]["filePath"])
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[0]["filePath"]))

@cross_origin()
@app.route(f"/{API_BASEPATH}/sample/count/people", methods=[QUERIES[1]["method"]])
def countSamplesInGraphByPeople():
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[1]["filePath"]))

@cross_origin()
@app.route(f"/{API_BASEPATH}/sample/count/countries", methods=[QUERIES[2]["method"]])
def countSamplesInGraphByCountries():
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[2]["filePath"]))

@cross_origin()
@app.route(f"/{API_BASEPATH}/organ", methods=[QUERIES[3]["method"]])
def listAvailableOrgansForSpecieName():
    specieName = request.json["specie_name"]
    query_parameters = [ {"string_to_replace": "Homo sapiens", "values": [specieName]} ]
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[3]["filePath"], query_parameters))

## Compentency questions
@cross_origin()
@app.route(f"/{API_BASEPATH}/get-ktop-antibiotic-res-genes", methods=[QUERIES[4]["method"]])
def getKTopAntibioticResGenes():
    metric = request.json["metric"]
    query_parameters = [ {"string_to_replace": "Gene Length", "values": [metric]} ]
    return jsonify(executeQuery(SPARQL_ENDPOINT, QUERIES[4]["filePath"]))




## Launch the Flask app (the ABRomics-KG API)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=API_PORT, debug=True)
