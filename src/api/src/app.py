

## Config imports 
from config.config import *

## Route imports
from routes.base import *
from routes.admin import *
from routes.stats import *
from routes.abromics import *
from routes.competency_questions import *

## Module imports
from modules.graph_creator.graph_creator import GraphCreator


## On API start


## Launch the Flask app (the ABRomics-KG API)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=API_PORT, debug=True)
