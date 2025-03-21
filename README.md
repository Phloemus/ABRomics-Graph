# ABRomics KG 

Abromics KG correspond to the WP2.4 of the Abromics project, which should ensure the FAIR principles by using 
finding appropriate ontologies for Abromics usecases and setting up a knowledge graph to integrate more data
in the graph.

## Main goals of ABRomics KG

The ABRomics KG provide a graph with which the ABRomics platform can get data from and easily get access to 
informations available in external knowledge graphs provided by external data sources.

1. Provide graph structure for the ABRomics data that can support SPARQL request
2. Laverage the graph structure to access fine descriptions in external specific ontologies enriching the ABRomics database.
3. Provide a way to make requests to external knowledge graphs
4. Ensuring an interoperability between the ABRomics data and the data present in external knowledge graphs

## Parts of the project

To ensure the goal written previously, ABRomics KG is composed of multiple parts.

1. Virtuoso graph server
2. Developper API
3. SPARQL queries collection
4. Web dashboard

## Download the codebase of the project

To get the whole codebase of the ABRomics-kg project run:

### From gitlab.com

```
bash
git clone git@gitlab.com:ifb-elixirfr/abromics/abromics-graph.git
```

### From gitlab.univ-nantes.fr

```
bash 
git clone https://gitlab.univ-nantes.fr/BiRD/abromics-kg.git
```

## Production deploy 

First modify the **.env** file to fit your project. The values by default will work correctly when deploying the 
app using docker but in a production environment, don't forget to modify the api admin credentials  

To deploy the whole application (graph server, API and dashboard), you can use docker by running:

```
bash 
docker compose --env-file .env up -d
```

By default : 

- Web dashboard: [http://localhost:8081](http://localhost:8081)
- API: [http://localhost:8081/graph-api](http://localhost:8081/graph-api)
- Graph server: [http://localhost:8081/sparql](http://localhost:8081/sparql)

## Virtuoso graph server

## Developper API 

## SPARQL queries collection

## Web dashboard

### Graph structure

The design of the graph structure require to have a deep understanding of the underlying ontologies that are 
used to make such knowledge graph. The goal of the knowledge graph is to be a close representation of the 
data that are used in ABRomics as well as keeping the relations between the data. A knowledge graph define 
the structure that all data should be following. This is important to ensure that the data instanciated 
with the knowledge graph follows a consistant structure, so users know how to retrive data from the graph
using SPARQL requests (which will be consistant as the sturcture of the graph is). 

Thus the structure of the graphs should:

1. Follow the terms of ontologies of references (ontologies that are already used by a lot of people and 
   which have their structure proven to be efficient to represent data)
2. Use the terms of the ontology that are relevant to the ABRomics project. This means that all the 
   data treatment made by ARBomics must be represented in a way in the knowledge graph

