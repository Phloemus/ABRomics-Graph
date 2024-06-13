#!/usr/bin/env python3

### Create the links between the people and the samples 

from rdflib import Graph
from rdflib import Namespace
from rdflib import FOAF, DCTERMS, SKOS, VANN, TIME, RDF, RDFS, XSD, OWL, Literal

## Load the people and samples files in rdflib
g = Graph()
g.parse('/home/brieuc/Documents/dev/abromics/abromics-kg/dev/analysis/out/people.ttl', format='ttl')
g.parse('/home/brieuc/Documents/dev/abromics/abromics-kg/dev/analysis/out/samples.ttl', format='ttl')

qryGetSample = """
    PREFIX

    SELECT ?sample

"""

qryGetSamplesSubmitters = """
    PREFIX prov: <http://www.w3.org/ns/prov#>

    SELECT ?people 
    WHERE {
        ?people rdf:type prov:Person .
    }
"""

res = g.query(qryGetSamplesSubmitters)

for row in res:
    print(f"{row.people}")


