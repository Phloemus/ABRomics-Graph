#!/usr/bin/env python3

### Module that creates the sosa graph from all the ABRomics reports

## Necessary imports
import json
import os
import uuid

from datetime import datetime
from jinja2 import Environment, FileSystemLoader, StrictUndefined

## Creator module class
class GraphCreator:

    def __init__(self, reportDirectory):
        self.reportDirectory = reportDirectory
        self.allReports = []
        
        ## entities
        self.people = []
        self.samples = []

        ## mappings help to track the link between entity from the reports and graph entities
        self.samplesMapping = {}
        self.peopleMapping = {}

        ## entities links
        self.samplesSubmitters = {}


    ##### Private methods #####

    ## Return the dictionnary of the data corresponding to a given json file
    def __readJsonFromFile(self, path):
        with open(path) as f:
            d = json.load(f)
            return d

    ## return a boolean indicating if the string parameter value has a correct datetime format
    def __isDatetime(self, val):
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    ## Add people data to memory for graph creation
    def __addPeople(self):
        for report in self.allReports:
            if report["sections"][0]["data"][0]["values"][10] not in self.peopleMapping.keys():
                uniqueGraphId = uuid.uuid1()
                name = report["sections"][0]["data"][0]["values"][10]
                email = ""
            
                if len(report["sections"][0]["data"][0]["values"]) == 12:
                    email = report["sections"][0]["data"][0]["values"][11] 
            
                self.people.append({
                    "id": uniqueGraphId,
                    "name": name,
                    "email": email
                })

                self.peopleMapping[name] = uniqueGraphId

    ## Create the people entities in a ttl file
    def __createPeople(self):
        env = Environment(
            loader=FileSystemLoader('.'),
            undefined=StrictUndefined
        )
        template = env.get_template("graph-templates/people.j2") 
        templateVars = { "people" : self.people }
        peopleGraph = template.render(templateVars)
        with open("out/people.ttl", "w") as f:
            f.write(peopleGraph)
        print("People graph created in the ./out directory")

    ## Add the samples data to memory for graph creation
    def __addSamples(self):
        for report in self.allReports:
            if report["sections"][0]["data"][0]["values"][0] not in self.samplesMapping.keys():
                uniqueGraphId = uuid.uuid1()
                originalSampleId = report["sections"][0]["data"][0]["values"][0]
                submitterId = report["sections"][0]["data"][0]["values"][10]

                self.samples.append({
                    "id": uniqueGraphId,
                    "originalSampleId": originalSampleId,
                    "strainId": report["sections"][0]["data"][0]["values"][1],
                    "microorganismScientificName": report["sections"][0]["data"][0]["values"][2],
                    "collectionDate": report["sections"][0]["data"][0]["values"][3],
                    "sampleType": report["sections"][0]["data"][0]["values"][4],
                    "sampleSource": report["sections"][0]["data"][0]["values"][5],
                    "host": report["sections"][0]["data"][0]["values"][6],
                    "country": report["sections"][0]["data"][0]["values"][7],
                    "sequencingTechnology": report["sections"][0]["data"][0]["values"][8],
                    "sequencingPartner": report["sections"][0]["data"][0]["values"][9],
                    "submitterId": self.peopleMapping[submitterId]
                })

                self.samplesSubmitters[originalSampleId] = submitterId
                self.samplesMapping[originalSampleId] = uniqueGraphId

    ## Create the samples entities in a ttl file
    def __createSamples(self):
        env = Environment(
            loader=FileSystemLoader('.'),
            undefined=StrictUndefined
        )
        env.filters['isDatetime'] = self.__isDatetime
        template = env.get_template("graph-templates/samples.j2") 
        templateVars = { "samples" : self.samples }
        sampleGraph = template.render(templateVars)
        with open("out/samples.ttl", "w") as f:
            f.write(sampleGraph)
        print("Samples graph created in the ./out directory")


    ##### Public methods #####

    def createGraph(self):
        self.allReports = [self.__readJsonFromFile(f"{self.reportDirectory}/{reportFilename}") for reportFilename in os.listdir("reports") if reportFilename.endswith(".json")]
        self.__addPeople()
        self.__createPeople()
        self.__addSamples()
        self.__createSamples()
        
        


## Usecase of the graph creator
gc = GraphCreator("reports")
gc.createGraph()
