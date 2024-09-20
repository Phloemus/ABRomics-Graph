#!/usr/bin/env python3


## Necessary imports
import os

from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Union
from fastapi import FastAPI

## Module imports
from modules.graph-creator import graph-creator as GraphTools

app = FastAPI(debug=True)
sparqlEndpoint = "https://abromics.gcp.glicid.fr/sparql"

@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/count-nodes") 
def countNodes():
    sparql_query = """
       SELECT ?graph (COUNT(?s) AS ?triples)
       WHERE {
          GRAPH ?graph {
            ?s ?p ?o .
          }
        }
        GROUP BY ?graph
    """
    sparql = SPARQLWrapper(sparqlEndpoint)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(sparql_query)
    try:
        res = sparql.query().convert()
        recs = res["results"]["bindings"]
    except Exception as e:
        return {"error-message": e}
    response = list()
    for item in recs:
        response.append({"graphName": item["graph"]["value"], "nbTriples": item["triples"]["value"]})
    return response


## The specie name could be the common name or latin name
@app.get("/get-organs/{specie_name}") 
def getOrgans(specie_name: str):
    sparql_query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ncbitaxon: <http://purl.obolibrary.org/obo/NCBITaxon_>
        PREFIX uberon: <http://purl.obolibrary.org/obo/UBERON_>
        PREFIX obom: <https://data.bioontology.org/metadata/obo/>
        PREFIX ro: <http://purl.obolibrary.org/obo/RO_>
        
        SELECT ?specie ?organs ?organLabels WHERE {{
          ?specie rdfs:label "{ specie_name }" .
          ?organs ro:0002175 ?specie . ## ro:0002175 indicates the "present_in_taxon" ontology
          ?organs rdfs:label ?organLabels .
        }}
    """
    sparql = SPARQLWrapper(sparqlEndpoint)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(sparql_query)
    try:
        res = sparql.query().convert()
        recs = res["results"]["bindings"]
    except Exception as e:
        return {"error-message": e}
    response = list()
    for item in recs:
        response.append({"specie": item["specie"]["value"], "organ": item["organs"]["value"], "organName": item["organLabels"]["value"]})
    return response


## Allow to create the graph files 
@app.get("/create-graph")
def createGraph():
    gc = GraphTools.GraphCreator("reports")
    gc.createGraph()



