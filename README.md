# ABRomics graph

Abromics graph correspond to the WP2.4 of the Abromics project, which should ensure the FAIR principles by using 
finding appropriate ontologies for Abromics usecases and setting up a knowledge graph to integrate more data
in the graph.

## Main goals of ABRomics graph

ABRomics graph provide a knowledge graph for the ABRomics platform. The ABRomics graph has 4 main objectives:

1. Provide graph structure for the ABRomics data that can support SPARQL request
2. Use terms from relevant ontologies in the domain of antibiotic resistance
3. Link the ABRomics data with external knowledge graph 
4. Ensuring an interoperability between the ABRomics data and the data present in external knowledge graphs

## Parts of the project

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

## Development deployment

First modify the variables in **.env** file to fit your project. The values by default will work correctly 
when deploying the app using docker.

To deploy the whole application (graph server, API and dashboard), you can use docker by running:

```
bash 
docker compose --env-file .env up -d
```

By default : 

- Web dashboard: [http://localhost:8081](http://localhost:8081)
- API: [http://localhost:8081/graph-api](http://localhost:8081/graph-api)
- Graph server: [http://localhost:8081/sparql](http://localhost:8081/sparql)

## Production deployment

To deploy the application in a production environement use the **.env.prod** file instead. 

> [!NOTE]
> Do not forget to change the admin credentials ! 

```
bash 
docker compose --env-file .env.prod up -d
```

## Virtuoso graph server

The virtuoso graph server respond to SPARQL queries sent to [http://localhost:8081/sparql](http://localhost:8081/sparql). This sparql endpoint holds all the public data of ABRomics and is accessible publicly to request using SPARQL queries.

See more [developper documentation](https://gitlab.com/ifb-elixirfr/abromics/abromics-graph/-/blob/main/src/graph/README.md) about the virtuoso graph server

## Developper API 

The API allows any plateform to perform execute some predefined sparql queries on the knowledge graph without 
needing to write SPARQL queries.

See more [developper documentation](https://gitlab.com/ifb-elixirfr/abromics/abromics-graph/-/blob/main/src/api/README.md)

## SPARQL queries collection

A SPARQL queries collection is available [here](https://gitlab.com/ifb-elixirfr/abromics/abromics-graph/-/blob/main/queries) to test the knowledge graph 

See the [documentation](https://gitlab.com/ifb-elixirfr/abromics/abromics-graph/-/blob/main/queries/README.md) of the structure of the knowledge graph of ABRomics

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

