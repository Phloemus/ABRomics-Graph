#!/usr/bin/env python3

### Module that creates the sosa graph from all the ABRomics reports

## Necessary imports
import json
import os
import uuid

from datetime import datetime
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from SPARQLWrapper import SPARQLWrapper, JSON

## Creator module class
class GraphCreator:

    def __init__(self, reportDirectory):
        self.reportDirectory = reportDirectory
        self.allReports = []

        ## entities
        self.platforms = []
        self.sensors = []
        self.procedures = []
        self.people = []
        self.samples = []

        ## external entities
        self.countries = {}
        self.regions = {}

        ## mappings help to track the link between entity from the reports and graph entities
        self.platformsMapping = {}
        self.sensorsMapping = {}
        self.proceduresMapping = {}
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

    ## Write a dictionnary to a json file 
    def __writeCacheToJson(self, dictionnary, path):
        if not os.path.exists("cache"):
            os.makedirs("cache")
        with open(path, 'w') as file:
            json.dump(dictionnary, file, indent=4)

    ## return a boolean indicating if the string parameter value has a correct datetime format
    def __isDatetime(self, val):
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    ## Get the countries from wikidata
    ## returns dictionnary of countries name corresponding wikidata ids
    def __getCountries(self, from_cache=False):
        if from_cache is False:
            sparql_query = """
                SELECT ?countryId ?countryName WHERE {
                        ?countryId wdt:P31 wd:Q6256 . 
                        ?countryId rdfs:label ?countryName .
                        FILTER (lang(?countryName) = "en")
                        }
            """
            print("Fetching countries wikidata ids ...")
            sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
            sparql.setReturnFormat(JSON)
            sparql.setQuery(sparql_query)
            try:
                res = sparql.query().convert()
                recs = res["results"]["bindings"]
            except Exception as e:
                print(e)
            for item in recs:
                self.countries[item["countryName"]["value"]] = item["countryId"]["value"] ## All countries are in self.countries now !
                self.__writeCacheToJson(self.countries, "cache/countries.json")
        else:
            self.countries = self.__readJsonFromFile("cache/countries.json")

    ## Get the regions from wikidata
    ## returns dictionnary of regions name corresponding to wikidata ids
    ## TODO: Link the regions to the sample
    def __getRegions(self):
        sparql_query = """
            SELECT ?regionId ?regionName WHERE {
                    ?regionId wdt:P31 wd:Q56061 ;
                    wdt:P17 ?country .
                    ?regionId rdfs:label ?regionName .
                    }
        """
        print("Fetching regions wikidata ids ...")
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(sparql_query)
        try:
            res = sparql.query().convert()
            recs = res["results"]["bindings"]
        except Exception as e:
            print(e)
        for item in recs:
            self.regions[item["regionName"]["value"]] = item["regionId"]["value"]

    ## Add the plateforms (places where the workflows were performed)
    def __addProcedures(self):
        uniqueGraphId = uuid.uuid1()
        name="wf1"

        self.procedures.append({
            "id": uniqueGraphId,
            "isImplementedBy": self.sensorsMapping["genomic"]
        })

        self.platformsMapping[name] = uniqueGraphId

    ## Create all added procedures
    def __createProcedures(self):
        env = Environment(
            loader=FileSystemLoader('.'),
            undefined=StrictUndefined
        )
        template = env.get_template("graph-templates/procedures.j2")
        templateVars = { "procedures" : self.procedures }
        proceduresGraph = template.render(templateVars)
        with open("out/procedures.ttl", "w") as f:
            f.write(proceduresGraph)
        print("Procedures graph created in the ./out directory")

    ## Add the plateforms (places where the workflows were performed)
    def __addPlatforms(self):
        uniqueGraphId = uuid.uuid1()
        name="NNCR"

        self.platforms.append({
            "id": uniqueGraphId,
        })

        self.platformsMapping[name] = uniqueGraphId

    ## Create all added platforms
    def __createPlatforms(self):
        env = Environment(
                loader=FileSystemLoader('.'),
                undefined=StrictUndefined
                )
        template = env.get_template("graph-templates/platforms.j2")
        templateVars = { "platforms" : self.platforms }
        platformsGraph = template.render(templateVars)
        with open("out/platforms.ttl", "w") as f:
            f.write(platformsGraph)
        print("Sensors graph created in the ./out directory")

    ## Add sensors data to memory for graph creation
    ## Sensors define the workflow used in to produce de reports (default genomic)
    def __addSensors(self):
        uniqueGraphId = uuid.uuid1()
        name="genomic"

        self.sensors.append({
            "id": uniqueGraphId,
            "implements": "abromics:WF1_spec",
            "isHostedBy": self.platformsMapping["NNCR"]
        })

        self.sensorsMapping[name] = uniqueGraphId

    ## Create all added sensors
    def __createSensors(self):
        env = Environment(
                loader=FileSystemLoader('.'),
                undefined=StrictUndefined
                )
        template = env.get_template("graph-templates/sensors.j2") 
        templateVars = { "sensors" : self.sensors }
        sensorsGraph = template.render(templateVars)
        with open("out/sensors.ttl", "w") as f:
            f.write(sensorsGraph)
        print("Sensors graph created in the ./out directory")

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
                countryName = report["sections"][0]["data"][0]["values"][7]

                self.samples.append({
                    "id": uniqueGraphId,
                    "originalSampleId": originalSampleId,
                    "strainId": report["sections"][0]["data"][0]["values"][1],
                    "microorganismScientificName": report["sections"][0]["data"][0]["values"][2],
                    "collectionDate": report["sections"][0]["data"][0]["values"][3],
                    "sampleType": report["sections"][0]["data"][0]["values"][4],
                    "sampleSource": report["sections"][0]["data"][0]["values"][5],
                    "host": report["sections"][0]["data"][0]["values"][6],
                    "country": self.countries[countryName] if countryName in self.countries.keys() else "",
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


    ##### Public test methods #####

    ## Checks if a region name is findable in the regions fetched from wikidata
    ## returns bool
    def isRegionExists(self, regionName):
        if regionName in self.regions.keys():
            print(f"Region {regionName} exists ! -> {self.regions[regionName]}")
            return True
        else:
            print(f"Region {regionName} doesn't exist")
        return False

    ##### Public methods #####

    def createGraph(self):
        choiceCountries = input("Get fresh countries data (from wikidata) ? [yes/no] ")
        if choiceCountries == "yes": 
            self.__getCountries(from_cache=False)
        else:
            self.__getCountries(from_cache=True)
        self.allReports = [self.__readJsonFromFile(f"{self.reportDirectory}/{reportFilename}") for reportFilename in os.listdir("reports") if reportFilename.endswith(".json")]
        self.__addPlatforms()
        self.__addSensors()
        self.__addProcedures()
        self.__createPlatforms()
        self.__createSensors()
        self.__createProcedures()
        self.__addPeople()
        self.__createPeople()
        self.__addSamples()
        self.__createSamples()



## Usecase of the graph creator
gc = GraphCreator("reports")
gc.createGraph()
