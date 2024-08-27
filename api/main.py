#!/usr/bin/env python3


## Necessary imports
import os

from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Union
from fastapi import FastAPI

app = FastAPI()

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
    sparql = SPARQLWrapper("http://localhost:8081/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(sparql_query)
    try:
        res = sparql.query().convert()
        return res
    except Exception as e:
        return {"error-message": e}
