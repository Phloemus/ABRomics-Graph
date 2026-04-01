
## Query util functions
##
## All the methods that allows to manipulate and execute a sparql query on the knowledge graph
##
## methods:
## - __prepareQuery: (private method) allows to replace the variables present inside the 
##                   queries by the parameter values
##
## - executeQuery: execute the query defined in the queryFile on the sparql endpoint 
##                 and return the records that were given as the knowledge graph response
##                 or return the error status and error associated message
## 


from SPARQLWrapper import SPARQLWrapper, JSON
import json

## Config imports
from config.config import *
## from utils.cache import BinaryTrieCache ## Cache not mature now


## A query object that contains the content of a query and methods to execute such query on the targeted SPARQL endpoint
## Basic use: 
## From a raw string (default) :     Query(queryString, sparqlEndpoint)
## From a query file           :     Query.fromFile(queryFilePath, sparqlEndpoint, parameters)
class Query():

    def __init__(self, queryString, sparqlEndpoint=""): 
        self.sparqlEndpoint = sparqlEndpoint
        self.queryString = queryString 
    
    @classmethod
    def fromFile(cls, queryFilePath, sparqlEndpoint="", parameters={}):
        with open(queryFilePath, 'r') as file:
            query = file.read()

        for key, value in parameters.items():
            query = query.replace(f"${key}", f"'{value}'")

        return cls(queryString=query, sparqlEndpoint=sparqlEndpoint)

    
    def executeQuery(self):
        
        sparql = SPARQLWrapper(self.sparqlEndpoint)
        sparql.setReturnFormat(JSON)
        sparql.setQuery(self.queryString)
        try:
            res = sparql.query().convert()
            recs = res["results"]["bindings"]
            return recs
        except Exception as e:
            print(e)
            return {"status": "error", "message": str(e), "endpoint": self.sparqlEndpoint}


    def exportQueryResult(self, filePath):

        recs = self.executeQuery()

        if "status" in recs and recs["status"] == "error":
            return Exception
        else:
            records = {}
            count = 0
            for rec in recs:
                recordDict = {
                    "class": rec["class"]["value"],
                    "specieName": rec["specieName"]["value"]
                }
                records[count] = recordDict
                count = count + 1
            with open(filePath, 'w+') as f:
                json.dump(records, f)
