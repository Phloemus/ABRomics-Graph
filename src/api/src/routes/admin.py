
## Admin routes
##
## Routes that can only be used by an admin to perform routine operations on the knowledge graph
##
## routes:
## - [POST] graph-api/login (not protected)
## - [POST] graph-api/protected (protected - for test purposes)
## - [DELETE] graph-api/graph (protected)

import jwt
import datetime
from flask import jsonify, request, make_response
from flask_cors import cross_origin

## Config imports
from config.config import *
from config.constants import *

## Util imports
from utils.authentification import *
from utils.query import Query



########################################## Login route ###############################################
@app.route(f"/{API_BASEPATH}/login", methods=['POST'])
def login():
    username = request.json["username"]
    password = request.json["password"]
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3)}, app.config['secret_key'])
        return jsonify({"token": token})
    else:
        return make_response(jsonify({"message": "wrong username or password"}), 401)


######################################## Protected route #############################################
@app.route(f"/{API_BASEPATH}/protected", methods=['POST'])
@authentification_required
def protected():
    return jsonify({"message": "protected route tested"})


####################################### Delete graph route ###########################################
@app.route(f"/{API_BASEPATH}/graph", methods=['DELETE'])
@authentification_required 
def deleteGraphData():
    executeQuery(SPARQL_ENDPOINT, ADMIN_QUERIES[0]["filePath"])
    return jsonify({"message": "graph delete successfully"})


####################################### Recreate graph route #########################################
## This should be implemented after that the graph creator module has been tested
@cross_origin()
@app.route(f"/{API_BASEPATH}/graph", methods=['POST'])
@authentification_required 
def buildGraph():
    gc = GraphCreator(reportDirectory = "data/reports", sparqlEndpoint = "http://localhost:8890/sparql") ## replace the localhost:8890 with a flexible link to the virtuoso server
    gc.createGraph(fetchCountriesFromCache = False, templatePath="modules/graph_creator/", outputPath="modules/graph_creator/out")
    print("ok")
    return jsonify({"message": "test 1 passed"})



