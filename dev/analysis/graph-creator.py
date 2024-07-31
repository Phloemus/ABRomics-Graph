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
        self.species = []
        self.strains = []
        self.sampleSources = []

        ## external entities and mappings between entities and ontology identifiers
        self.countries = {}
        self.regions = {}
        self.speciesTaxonomy = {}  # bind species with NCBI Taxon ontology terms
        self.sampleSourcesBindNCIT = {}    # bind sampleSources with NCIT terms

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

    def __createTtlFile(self, templatePath, dataName, data, filterFunctions=[]):

        """
          Create the ttl file from a template and the data
          
          templatePath: path to the template file used to create the ttl file from the data
          dataName: name used to qualify the data present in the entities variables
          data: content of an entity variable

          filterFunctions: 
               (ex: [{"name": "isDatetime", "content": self.__isDatetime}])
               contains a list of objects each containing a function that is passed to 
               jinja as a filter function
        """

        env = Environment(
            loader=FileSystemLoader('.'),
            undefined=StrictUndefined
        )
        for function in filterFunctions:
            env.filters[function["name"]] = function["content"]
        template = env.get_template(templatePath)
        templateVars = { dataName : data }
        dataGraph = template.render(templateVars)
        with open(f"out/{dataName}.ttl", "w") as f:
            f.write(dataGraph)
        print(f"{dataName} graph created")


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


    ## Get the sample sources from the NCIT ontology hosted by the ncit browser ######################################################
    ## Doesn't really works ..
    ## The response of the query doesn't seems to be right ..
    ## All the issues to create the query and now with the issue that seems to be caused by the format of the query 
    ## could be solved by getting the NCIT ontology directly onto the virtuoso server
    def __getSampleSources(self):
        for report in self.allReports:
            self.sampleSources.append(report["sections"][0]["data"][0]["values"][5])
        sampleSourceNames = ""
        for sampleSourceName in self.species:
            sampleSourceNames += f"'{sampleSourceName}' "
        sparql_query = f"""
            SELECT ?sampleSourceName ?sourceId WHERE {{
                VALUES ?sampleSourceName {{
                    "{sampleSourceNames}"^^<http://www.w3.org/2001/XMLSchema#string> 
                }}
                ?sourceId rdfs:label ?sampleSource .
                FILTER STRSTARTS(STR(?sourceId), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") .
            }}
        """
        print("Fetching sample source ids ...")
        sparql = SPARQLWrapper("https://sparql.hegroup.org/sparql")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(sparql_query)
        try:
            res = sparql.query().convert()
            recs = res["results"]["bindings"]
            for item in recs:
                print(item)
                print(f"- binding {item['sourceSampleName']['value']} with {item['sourceId']['value']} -")
                self.sampleSourcesBindNCIT[item["sampleSourceName"]["value"]] = item["sourceId"]["value"]
        except Exception as e:
            print(e)
        

    ## Get the ncbi taxon id of a list of species
    def __getSpeciesTaxonomy(self):
        for report in self.allReports:
            # add the microorganisms in the species dictionnary
            if report["sections"][1]["data"][0]["values"][0] not in self.species:
                self.species.append(report["sections"][1]["data"][0]["values"][0])
            # add the host specie to the species dictionnary
            if report["sections"][0]["data"][0]["values"][6] not in self.species: 
                self.species.append(report["sections"][0]["data"][0]["values"][6])
        speciesNames = ""
        for speciesName in self.species:
            speciesNames += f"'{speciesName}' "
        sparql_query = f"""
            PREFIX up: <http://purl.uniprot.org/core/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT ?speciesName ?taxon
            WHERE {{
              VALUES ?speciesName {{
                  {speciesNames}
              }}
              
              ?taxon a up:Taxon ;
                     up:scientificName ?speciesName .
            }}
        """
        print("Fetching species taxonomy ids ...")
        sparql = SPARQLWrapper("https://sparql.uniprot.org/sparql/")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(sparql_query)
        try:
            res = sparql.query().convert()
            recs = res["results"]["bindings"]
        except Exception as e:
            print(e)
        for item in recs:
            self.speciesTaxonomy[item["speciesName"]["value"]] = item["taxon"]["value"]

    ## Add the plateforms (places where the workflows were performed)
    def __addProcedures(self):
        uniqueGraphId = uuid.uuid1()
        name="wf1"

        self.procedures.append({
            "id": uniqueGraphId,
            "isImplementedBy": self.sensorsMapping["genomic"]
        })

        self.platformsMapping[name] = uniqueGraphId

    ## Add the plateforms (places where the workflows were performed)
    def __addPlatforms(self):
        uniqueGraphId = uuid.uuid1()
        name="NNCR"

        self.platforms.append({
            "id": uniqueGraphId,
        })

        self.platformsMapping[name] = uniqueGraphId

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

    ## Add strains data to memory for graph creation
    def __addStrains(self):
        for report in self.allReports:
            uniqueGraphId = uuid.uuid1()
            speciesName = report["sections"][1]["data"][0]["values"][0]
            st = report["sections"][1]["data"][0]["values"][1]
            taxonomy = self.speciesTaxonomy[speciesName]

            self.strains.append({
                "id": uniqueGraphId,
                "st": st,
                "taxonomy": taxonomy
            })

    ## Add genes data to the memory for graph creation
    ## should get all the gene ontology id from the gene names to have fair data !
    def __addGenes(self):
        pass

    ## Add the samples data to memory for graph creation
    def __addSamples(self):
        for report in self.allReports:
            if report["sections"][0]["data"][0]["values"][0] not in self.samplesMapping.keys():
                uniqueGraphId = uuid.uuid1()
                originalSampleId = report["sections"][0]["data"][0]["values"][0]
                submitterId = report["sections"][0]["data"][0]["values"][10]
                countryName = report["sections"][0]["data"][0]["values"][7]
                microorganism = report["sections"][0]["data"][0]["values"][2]
                host = report["sections"][0]["data"][0]["values"][6]
                sampleSource = report["sections"][0]["data"][0]["values"][5]

                self.samples.append({
                    "id": uniqueGraphId,
                    "originalSampleId": originalSampleId,
                    "strainId": report["sections"][0]["data"][0]["values"][1],
                    "microorganism": self.speciesTaxonomy[microorganism] if microorganism in self.speciesTaxonomy.keys() else "",
                    "collectionDate": report["sections"][0]["data"][0]["values"][3],
                    "sampleType": report["sections"][0]["data"][0]["values"][4],
                    "sampleSource": "amelioration en cours", ####################### Sample source bind to relevant ontology
                    "host": self.speciesTaxonomy[host] if host in self.speciesTaxonomy.keys() else "",
                    "country": self.countries[countryName] if countryName in self.countries.keys() else "",
                    "sequencingTechnology": report["sections"][0]["data"][0]["values"][8],
                    "sequencingPartner": report["sections"][0]["data"][0]["values"][9],
                    "submitterId": self.peopleMapping[submitterId]
                })

                self.samplesSubmitters[originalSampleId] = submitterId
                self.samplesMapping[originalSampleId] = uniqueGraphId

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

        ## Loading the reports in memory
        self.allReports = [self.__readJsonFromFile(f"{self.reportDirectory}/{reportFilename}") for reportFilename in os.listdir("reports") if reportFilename.endswith(".json")]

        ## Getting static values
        choiceCountries = input("Get fresh countries data (from wikidata) ? [yes/no] ")
        if choiceCountries == "yes": 
            self.__getCountries(from_cache=False)
        else:
            self.__getCountries(from_cache=True)
        self.__getSpeciesTaxonomy()
        self.__getSampleSources()

        ## Adding entity data in memory 
        self.__addPlatforms()
        self.__addSensors()
        self.__addProcedures()
        self.__addPeople()
        self.__addStrains()
        self.__addSamples()

        ## Creating the turtle files
        self.__createTtlFile("graph-templates/platforms.j2", "platforms", self.platforms) 
        self.__createTtlFile("graph-templates/sensors.j2", "sensors", self.sensors) 
        self.__createTtlFile("graph-templates/procedures.j2", "procedures", self.procedures) 
        self.__createTtlFile("graph-templates/people.j2", "people", self.people) 
        self.__createTtlFile("graph-templates/strains.j2", "strains", self.strains)
        self.__createTtlFile("graph-templates/samples.j2", "samples", self.samples, filterFunctions=[{"name": "isDatetime", "content": self.__isDatetime}])



## Usecase of the graph creator
gc = GraphCreator("reports")
gc.createGraph()
