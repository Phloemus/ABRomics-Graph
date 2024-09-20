# Streamlit demo app

This is a small demo of the graph. It shows the structure of the graph as well as interesting queries that can 
be performed using SPARQL requests on the abromics knowledge graph.

## Launch the application standalone

It's possible to launch the streamlit app without the other services listed in docker compose. 


### Install the conda environement

```
bash
conda env create --name abr-streamlit -f environement.yaml
```

### Activate the conda environement

```
bash
conda activate abr-streamlit 
## or
source activate abr-streamlit 
```

### Launch the application in development mode

```
bash 
cd app
streamlit run Home.py --server.port=8502 --server.address=0.0.0.0
```
