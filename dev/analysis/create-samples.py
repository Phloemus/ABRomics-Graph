#!/usr/bin/env python3

### Create the samples.ttl file from the ABRomics reporst

import json
import os

from datetime import datetime
from jinja2 import Environment, FileSystemLoader, StrictUndefined

env = Environment(
    loader=FileSystemLoader('.'),
    undefined=StrictUndefined
)

## return a boolean indicating if the string parameter value has a correct datetime format
def isDatetime(val):
    try:
        datetime.strptime(val, "%Y-%m-%d")
        return True
    except ValueError:
        return False

## Return the dictionnary of the data corresponding to a given json file
def readJsonFromFile(path):
    with open(path) as f:
        d = json.load(f)
        return d

## Return a sample Uri
def generateSampleUri(sampleId):
    return f"http://abromics/sample#{sampleId}"

## Make utility function accessible from jinja
env.filters['isDatetime'] = isDatetime
env.filters['generateSampleUri'] = generateSampleUri

template = env.get_template('graph-templates/samples.j2')

allReports = [readJsonFromFile(f"reports/{reportFilename}") for reportFilename in os.listdir("reports") if reportFilename.endswith(".json")]

templateVars = {
            "samples": [allReports[x]["sections"][0]["data"][0] for x in range(0, len(allReports))],
            } 

## Generate the ttl file
renderedTemplate = template.render(templateVars)
with open('out/samples.ttl', 'w') as f:
    f.write(renderedTemplate)
print("The graph has been created in the ./out directory")
 
