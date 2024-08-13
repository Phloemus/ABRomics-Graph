# ABRomics-kg API 

The ABRomics KG API is a REST API allowing to perform queries and requests to the knowledge graph 
without ever needing to write a SPARQL query.

## Technical details

The ABRomics KG API relies on FastAPI.  

## Installation

Use a conda environnement or equivalent. Install the necessary dependancies 
included in the **requirements.txt** file

```
bash
# with conda
conda create --name fastapi -f requirements.txt
```

## Activate the environment

```
bash
source activate fastapi
```

## Running the server

To run the API server just use the command

```
bash
uvicorn main:app --reload --port 8080
```

The server runs at **http://127.0.0.1:8080** 
Add any endpoint to this url to get to the different routes of the API

## Get the documentation

To access to the swagger documentation of the API, simply go to **http://127.0.0.1:8080/docs**
