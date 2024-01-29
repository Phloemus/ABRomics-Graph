# ABRomics-kg API 

This API allows to perform CRUD requests on the ABRomics knowledge graph.

## Installation

Use a conda environnement or equivalent. Install the necessary dependancies 
included in the **environment.yml** file

```
bash
# with conda
conda env create -f environment.yml
```

## Running the server

To run the API server just use the command

```
bash
uvicorn main:app --reload
```

The server runs at **http://127.0.0.1:8000** 
Add any endpoint to this url to get to the different routes of the API

## Get the documentation

To access to the swagger documentation of the API, simply go to **http://127.0.0.1:8000/docs**