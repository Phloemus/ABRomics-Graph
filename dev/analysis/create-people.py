#!/usr/bin/env python3

### Create the people.ttl file from the ABRomics reporst

import json
import os

from datetime import datetime
from jinja2 import Environment, FileSystemLoader, StrictUndefined

env = Environment(
    loader=FileSystemLoader('.'),
    undefined=StrictUndefined
)

## Return the dictionnary of the data corresponding to a given json file
def readJsonFromFile(path):
    with open(path) as f:
        d = json.load(f)
        return d

## Return a sample Uri
def generatePersonUri(personId):
    return f"http://abromics/person#{personId}"

## Make utility function accessible from jinja
env.filters['generatePersonUri'] = generatePersonUri

template = env.get_template('graph-templates/people.j2')

allReports = [readJsonFromFile(f"reports/{reportFilename}") for reportFilename in os.listdir("reports") if reportFilename.endswith(".json")]

## Extract the people data from the reports
peopleNames = []
people = []
count = 1
for report in allReports:
    if report["sections"][0]["data"][0]["values"][10] not in peopleNames:
        name = report["sections"][0]["data"][0]["values"][10]
        email = ""
        peopleNames.append(name)

        if len(report["sections"][0]["data"][0]["values"]) == 12:
            email = report["sections"][0]["data"][0]["values"][11] 

        people.append({
            "id": count,
            "name": name,
            "email": email
        })
        count = count + 1

templateVars = {
    "people": people
} 

## Generate the ttl file
renderedTemplate = template.render(templateVars)
with open('out/people.ttl', 'w') as f:
    f.write(renderedTemplate)
print("The graph has been created in the ./out directory")
 
