<p align="center">
   <h1>ABRomics Graph</h1>
   <a href="https://10-54-3-233.gcp.glicid.fr/" target="_blank" rel="noopener">
      <img src="https://camo.githubusercontent.com/1423d8d34a668eb6efe1b0fc416c0b155d94610660d468b1d4fdf44dc740f54e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4275696c745f576974682d446f636b65722d696e666f726d6174696f6e616c3f7374796c653d666c6174266c6f676f3d646f636b6572" alt="Abromics Graph - A knowledge graph that links microbiome data" />
   </a>
</p>

# Abromics graph

Abromics graph is a knowledge graph model that allows to perform complex queries on heterogeneous microbiome data extracted from animal, enironmental and human samples. 
Fitting the one health approach, the project was first focused on antibiotic resistance data extracted from the [ABRomics platform](https://abromics.fr). With a simple and flexible 
knowledge graph structure, Abromics graph is a prime model to use in order to integrate more complex microbiome data while limiting query complexity.

## Main goals of Abromics graph

Abromics graph provide a knowledge graph for the Abromics platform. The Abromics graph has 4 main objectives:

1. Provide graph structure for the Abromics data that can support SPARQL request
2. Use terms from relevant ontologies in the domain of antibiotic resistance
3. Link the Abromics data with external knowledge graph 
4. Ensuring an interoperability between the Abromics data and the data present in external knowledge graphs

## Parts of the project

1. Graph server
2. Developper API
3. SPARQL queries collection
4. Web dashboard

## Download the codebase of the project

To get the whole codebase of the ABRomics-kg project run:

### From github.com

```
bash
git clone git@github.com:Phloemus/ABRomics-Graph.git
```

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

First make sure you have the **.env.dev** file in the git repo of the project. Its default values will work correctly 
for a standard development deployment of the whole application using docker

To deploy the whole application (graph server, API and dashboard), you can use docker by running:

```
bash 
docker compose --env-file .env up -d
```

By default : 

- Web dashboard: [http://localhost:8081](http://localhost:8081)
- API: [http://localhost:8081/graph-api](http://localhost:8081/graph-api)
- Graph server: [http://localhost:8081/graphdb](http://localhost:8081/graphdb)

### Configuration of the graphdb instance and addition of graph data

After the launch of every service via docker, it's essential to add a valid license to in the graphdb instance. 
To do so, go to [http://localhost:8081/graphdb/](http://localhost:8081/graphdb/) and add a valid graphdb license by clicking on the red button indicating that there is no license associated with your graphdb repo. 

> [!NOTE]
> You can get a free graphdb license by going on [graphdb website](https://graphwise.ai/components/graphdb/) 

> [!NOTE]
> Moreover instead of using the web interface of graphdb you can directly upload the graphdb license file you got from the graphdb team by directly putting it in the ```./src/graph/``` directory
> and naming the file "*license*". (A *.gitignore* entry make you license private, it won't be commited with your contributions)

## Production deployment

Deploying the application in a production environment requires a little bit more setup. 

First, you as the application uses the HTTPS protocol when deployed in a production environment, you need to put your hand on SSL certificates. 
You can either generate your own self-signed SSL certificates with the following command: 

```
bash 
cd src/nginx-config
mkdir certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./certificates/nginx.key -out ./certificates/nginx.crt
```

This strategy is good for small production deployment but your traffic will be limited as a self-signed certificates is often flagged as malicious by web browsers. 

To solve this issue, you can get the SSL certificates from a certificate authority like [Let's encrypt](https://letsencrypt.org/) which gives browser valid SSL certificates for free
Make sure you place the SSL certificates in the ```./src/nginx-config/certificates``` directory to make them accessible to the nginx reverse proxy behind the Abromics graph application.

Then, verify that all the values in the ```.env.prod``` file are ok. Especially for the API admin credentials and the url of the application which you should change to your own.

To deploy the application in a production environement use the ```.env.prod``` file instead in the ```docker compose``` command

```
bash 
docker compose --env-file .env.prod up -d
```

> [!NOTE]
> Do not forget to change the API admin credentials ! 

## Graphdb server

The Graphdb server respond to SPARQL queries sent to [http://localhost:8081/sparql](http://localhost:8081/sparql). This sparql endpoint holds all the public data of ABRomics and is accessible publicly to request using SPARQL queries.

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

