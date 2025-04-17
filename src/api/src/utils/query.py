
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


class Query:

    def __init__(self, queryFilePath, sparqlEndpoint="", parameters = {}):

        self.queryFilePath = queryFilePath
        self.sparqlEndpoint = sparqlEndpoint
        self.parameters = parameters
        
        self.queryString = ""


    def __prepareQuery(self):
        with open(self.queryFilePath, 'r') as file:
            query = file.read()

        for key, value in self.parameters.items():
            query = query.replace(f"${key}", f"'{value}'")

        self.queryString = query

    
    def executeQuery(self):

        self.__prepareQuery()
        
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
            records = []
            for rec in recs:
                records.append({ rec["class"]["value"]: rec["specieName"]["value"] })
            with open(filePath, 'w+') as f:
                json.dump(records, f)
