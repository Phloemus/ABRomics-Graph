#!/usr/bin/env python3

### Create ttl files (aka graphs) from ABRomics reports

# The goal of this program is to generate a large graph by using the data contained in the 
# ABRomics reports. These generated graphs should then be used to make a comparison between 
# The way SOSA and RDF data cube both handle the data, compare queries execution time ect..

## Author : Brieuc Quemeneur
## Last update : 14th may 2024

## Environment to activate : source activate ontology-analysis

### Necessary imports

from dotenv import load_dotenv
import os
import requests
import json
import pandas as pd

from alive_progress import alive_bar
import time

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from datetime import datetime

### Checking for aleady generated graphs
print("Checking for existing graphs")
if len(os.listdir("out")) != 0:
    print("Looks like the output folder is not empty. There might be some graphs there.")
    print("Do you want to override them ? (yes/no)")
    userInput = input()
    if userInput != "yes":
        print("Program aborted")
        exit()


### Get the abromics reports from the ABRomics api and store them locally
load_dotenv() 

## load the environment variables
api_url = os.getenv('API_URL') 
api_username = os.getenv('API_USERNAME')
api_password = os.getenv('API_PASSWORD')
api_temp_basic_token = os.getenv('API_TEMP_BASIC_TOKEN')

## fetches the ids of the reports marked as ready_to_report from ABRomics API
response = requests.get(
    "https://analysis.abromics.fr/api/analysis/",
    params={'status': 'ready_to_report'},
    headers = {
        'Authorization': f"Basic {api_temp_basic_token}",
    }
)
exploitable_analysis = response.json()
exploitable_analysis_ids = [analysis["id"] for analysis in exploitable_analysis["results"]]

## Download all the ABRomics reports (!continue)
if not os.path.exists("reports"):
    os.makedirs("reports")
    
with alive_bar(len(exploitable_analysis_ids)) as bar:
    for report_id in exploitable_analysis_ids:
        if f"abr_report_{report_id}.json" not in os.listdir("reports"):
            print(f"downloading report {report_id}")
            response = requests.get(
                f"https://analysis.abromics.fr/api/analysis/{report_id}/report/",
                headers = {
                    'Authorization': f"Basic {api_temp_basic_token}",
                }
            )
            report = response.json()
        
            # save the reports in a local file
            with open(f'reports/abr_report_{report_id}.json', 'w') as f:
                json.dump(report, f)
            bar()
        else:
            print(f"skipping report {report_id} : exists already")
            bar()

### Using jinja templates to create the graph using the data present in each report
env = Environment(
    loader=FileSystemLoader('.'),
    undefined=StrictUndefined
)

## Define string conversion function that will be used in the template
def convertToFriendlyNodeName(value):
    value = value.replace(' ', '_')
    value = value.replace('%', 'percent')
    return value

## Return a list with only unique elements
def unique(elemList):
    return list(set(elemList))

## Return a concanetaded list from a list of n lists
def concatList(listOfLists):
    concatenatedList = list()
    for n in listOfLists:
        concatenatedList = concatenatedList + n
    return concatenatedList

## Return the key (position) of an element in from an list
def getKeyFromValue(val, l):
    key = l.index(val)
    return key

## return the type of variable given in parameter as a small string
def isType(val):
    return type(val).__name__

## return a boolean indicating if the string parameter value has a correct datetime format
def isDatetime(val):
    try:
        datetime.strptime(val, "%Y-%m-%d")
        return True
    except ValueError:
        return False

## Add the conversion functions to the jinja enviroment
env.filters['convertToFriendlyNodeName'] = convertToFriendlyNodeName
env.filters['unique'] = unique
env.filters['concatList'] = concatList
env.filters['getKeyFromValue'] = getKeyFromValue
env.filters['isType'] = isType
env.filters['isDatetime'] = isDatetime

## Looks for available templates for jinja
def isTemplateExists(templatePath):
    if os.path.exists(templatePath): 
        return True
    return False 

## Return the dictionnary of the data corresponding to a given json file
def readJsonFromFile(path):
    with open(path) as f:
        d = json.load(f)
        return d

## For SOSA
def buildSosaGraph():
    if isTemplateExists("graph-templates/sosa.j2"):
        template = env.get_template('graph-templates/sosa.j2')
        allReports = [readJsonFromFile(f"reports/{reportFilename}") for reportFilename in os.listdir("reports") if reportFilename.endswith(".json")]
        templateVars = {
            "graphCreationDate": datetime.now(),
            "samples": [allReports[x]["sections"][0]["data"] for x in range(0, len(allReports))],
            "analysisSummary": [allReports[x]["sections"][1]["data"] for x in range(0, len(allReports))],
            "species": [allReports[x]["sections"][1]["data"][0]["values"][0] for x in range(0, len(allReports))],
            "resistanceHeader": allReports[0]["sections"][2]["data"][0]["header"],
            "resistances": [allReports[x]["sections"][2]["data"][0]["values"] for x in range(0, len(allReports))],
            "allGenes": unique(concatList([allReports[x]["sections"][2]["data"][0]["values"][0] for x in range(0, len(allReports))]))
        }
        renderedTemplate = template.render(templateVars)
        with open('out/sosa.ttl', 'w') as f:
            f.write(renderedTemplate)
        print("The graph has been created in the ./out directory")
    else:
        print("no jinja template for sosa have been provided")

## For RDF data cube
def buildQbGraph():
    pass

### Decide which kind of graph should be generated (SOSA or RDF data cube)
print("Choose graph type to build: (1:SOSA / 2:QB / 3:both)")
graphType = input()

if graphType == "1":
    buildSosaGraph()
if graphType == "2":
    buildQbGraph()
if graphType == "3":
    buildSosaGraph()
    buildQbGraph()

