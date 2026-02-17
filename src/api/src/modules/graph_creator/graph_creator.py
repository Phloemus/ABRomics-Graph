#!/usr/bin/env python3

### Module that creates the sosa graph from all the ABRomics reports

## Necessary imports
import json
import os
import uuid

from datetime import datetime
from dateutil import parser
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from SPARQLWrapper import SPARQLWrapper, JSON
from dotenv import load_dotenv # to read the environment variables from the .env file



## Creator module class
class GraphCreator:

    def __init__(self, reportDirectories = [], cacheDirectory = "", sparqlEndpoint = ""):
        self.reportDirectories = reportDirectories
        self.cacheDirectory = cacheDirectory
        self.sparqlEndpoint = sparqlEndpoint
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
        self.observableProperties = []
        self.observations = []
        self.genes = []

        ## external entities and mappings between entities and ontology identifiers
        self.countries = {}
        self.regions = {}
        self.speciesTaxonomy = {}          # bind species with NCBI Taxon ontology terms
        self.sampleSourcesBindNCIT = {}    # bind sampleSources with NCIT terms
        self.genesAroClasses = {}               # bind genes with ARO terms

        ## mappings help to track the link between entity from the reports and graph entities
        self.platformsMapping = {}
        self.sensorsMapping = {}
        self.proceduresMapping = {}
        self.strainsMapping = {}
        self.samplesMapping = {}
        self.peopleMapping = {}
        self.observablePropertiesMapping = {}
        self.genesMapping = {}

        ## entities links
        self.samplesSubmitters = {}

        ## many to many links
        self.linksSamplesObservations = []

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

    ## return true if the number given as parameter is a floating number and returns false otherwise
    def __isFloat(self, val):
        return type(val).__name__ == "float"

    ## curate the reports and only keep the reports that contains all the required fields
    def __curateReports(self):
        curatedReports = []
        for report in self.allReports:
            if "sections" not in report or len(report["sections"][1]["data"][0]["values"]) < 8:
                continue
            curatedReports.append(report)
        self.allReports = curatedReports

    ## from a table materialized as report["sections"][x][data][y], returns the value associated with 
    ## the column name from header that match the label. 
    def __getValueFromColname(self, tableData, label):
        if len([id for id, value in enumerate(tableData["header"]) if value == label]) != 0: 
            headerId = [id for id, value in enumerate(tableData["header"]) if value == label][0]
            if headerId != None:
                return tableData["values"][headerId]
            else: 
                return ""
        else:
            return ""

    def __createTtlFile(self, templatePath, outputPath, dataName, data, filterFunctions=[]):

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
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        with open(f"{outputPath}/{dataName}.ttl", "w") as f:
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
            self.countries = self.__readJsonFromFile(f"{self.cacheDirectory}/countries.json")


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


    ## TODO: a place will be used in the acinetobacter usecase as the city
    ## the query get the place name and the country to get the city id from
    ## wikidata
    def __getCity(self):
        sparql_query ="""
            SELECT ?city ?cityLabel WHERE {
                ?city wdt:P31/wdt:P279* wd:Q515;  # ?city is an instance or subclass of city
                rdfs:label "CITY_NAME"@en;    # Replace CITY_NAME with the name of the city
                wdt:P17 wd:COUNTRY_ID .        # Replace COUNTRY_ID with the country's Wikidata ID
                SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
            LIMIT 1
        """
        print("Fetching city wikidata ids ...")
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(sparql_query)
        try:
            res = sparql.query().convert()
            recs = res["results"]["bindings"]
        except Exception as e:
            print(e)
        for item in recs:
            self.cities[item["regionName"]["value"]] = item["regionId"]["value"]


    ## Get the sample sources from the NCIT ontology hosted by the ncit browser ######################################################
    ## Doesn't really works ..
    ## The response of the query doesn't seems to be right ..
    ## All the issues to create the query and now with the issue that seems to be caused by the format of the query 
    ## could be solved by getting the NCIT ontology directly onto the virtuoso server
    ## 
    ## This feature should be completed with the addition of UBERON and ENVO (inspired by the query that get a good list 
    ## of sample sources)
    def __getSampleSources(self):
        for report in self.allReports:
            sampleSource = self.__getValueFromColname(report["sections"][1]["data"][0], "Sample source")
            if sampleSource != None and sampleSource != "":
                self.sampleSources.append(sampleSource)
        sampleSourceNames = ""
        for sampleSourceName in self.sampleSources:
            sampleSourceNames += f"'{sampleSourceName}' "
        sparql_query = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX ncbitaxon: <http://purl.obolibrary.org/obo/NCBITaxon_>
            PREFIX uberon: <http://purl.obolibrary.org/obo/UBERON_>
            PREFIX envo: <http://purl.obolibrary.org/obo/ENVO_>
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
            PREFIX sio: <http://semanticscience.org/resource/>

            SELECT DISTINCT  ?sampleSourceName ?sourceId ?parentClass ?parentClassLabel (COUNT(?existingSamples) as ?nbOccurences) 
            FROM <http://www.ontotext.com/explicit>
            WHERE {{
              {{ 
                ?sourceId rdfs:subClassOf+ uberon:0000465 . 
              }} UNION {{
                ?sourceId rdfs:subClassOf+ envo:00000428 .
              }} UNION {{
                 ?sourceId rdfs:subClassOf+ ncit:C12219 . ## ncit anatomical structure, system or substance
                MINUS {{
                  ?sourceId rdfs:subClassOf+ ?excluded .
                  VALUES ?excluded {{ ncit:C21599 ncit:C34070 }} . ## Exclude micro anatomical structure and cell part
                }}
              }} UNION {{
                ?existingSamples rdf:type sio:001050 .
                ?existingSamples prov:wasDerivedFrom ?sourceId .
              }}
              ?sourceId rdfs:label ?sampleSourceName .
              VALUES ?sampleSourceName {{
                    { sampleSourceNames }
              }}
              ?sourceId rdfs:subClassOf ?parentClass .
              ?parentClass rdfs:label ?parentClassLabel .
            }} GROUP BY ?sourceId ?sampleSourceName ?parentClass ?parentClassLabel
            ORDER BY DESC(?nbOccurences)
        """
        print("Fetching sample source ids ...")
        sparql = SPARQLWrapper("http://localhost:8081/graphdb/repositories/abromics-kg") ## This is in local : it's very baaad (but it has ARO indexed)
        sparql.setReturnFormat(JSON)
        sparql.setQuery(sparql_query)
        try:
            res = sparql.query().convert()
            recs = res["results"]["bindings"]
            print(recs)
            for item in recs:
                self.sampleSourcesBindNCIT[item["sampleSourceName"]["value"]] = item["sourceId"]["value"]
        except Exception as e:
            print(e)


    ## Get the ncbi taxon id of a list of species
    ## The SPARQL request is made on uniprot as uniprot-core contains the ids of ncbitaxon
    ## and uniprot is always up. So it's a great way to get the ids even though the abromics graph kg
    ## is not up yet (in which case, the ncbitaxon ontology present in the abromics graph is unaccessible)
    ## WARNING: the uniprot id present at the end of the url seems to match ncbi taxon. 
    ##          the solution would be to get the id and change the start of the url to ncbi taxon.
    def __getSpeciesTaxonomy(self):
        for report in self.allReports:
            microorganism =  self.__getValueFromColname(report["sections"][1]["data"][0], "Microorganism scientific name")
            host = self.__getValueFromColname(report["sections"][1]["data"][0], "Host")
            if microorganism not in self.species:
                self.species.append(microorganism)
            if host not in self.species: 
                self.species.append(host)
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
            ## only the ncbi taxon id
            taxon = item["taxon"]["value"].split("http://purl.uniprot.org/taxonomy/")[1] 
            self.speciesTaxonomy[item["speciesName"]["value"]] = taxon

    ## Get the list of the aro classes used for the genes
    ## warning : need a server with the aro ontology indexed accessible to perform the sparql query..
    def __getAroClasses(self):
        genesNames = ""
        genesNamesList = []
        for report in self.allReports:
            for genesName in report["sections"][3]["data"][0]["values"][0]:
                if genesName not in genesNamesList:
                    genesNames += f""""{genesName}" """
                    genesNamesList.append(genesName)
        sparql_query = f""" 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX aro: <http://purl.obolibrary.org/obo/ARO_>
            PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
            
            SELECT ?class ?genesName
            WHERE {{
              VALUES ?genesName {{
                  {genesNames}
              }}
              ?class rdfs:subClassOf+ aro:3000000 .
              ?class rdfs:label ?label .
              FILTER (lcase(str(?label)) = lcase(?genesName))
            }}
        """
        print("Fetching ARO classes...")
        print(sparql_query)
        sparql = SPARQLWrapper("http://localhost:8081/graphdb/repositories/abromics-kg") ## This is in local : it's very baaad (but it has ARO indexed)
        sparql.setReturnFormat(JSON)
        sparql.setQuery(sparql_query)
        try:
            res = sparql.query().convert()
            recs = res["results"]["bindings"]
        except Exception as e:
            print(e)
        for item in recs:
            self.genesAroClasses[item["genesName"]["value"]] = item["class"]["value"]
            print(self.genesAroClasses)



    ## Add the plateforms (places where the workflows were performed)
    ############################################################################################################################################# REWORK THIS FUNCTION
    def __addProcedures(self):
        uniqueGraphId = uuid.uuid1()
        name="workflow 1 (genomic)"
        sensorsList = filter(None, list(self.sensorsMapping.values()))

        self.procedures.append({
            "id": uniqueGraphId,
            "name": name,
            "isImplementedBy": sensorsList
        })

        self.proceduresMapping[name] = uniqueGraphId

    ## Add the plateforms (places where the workflows were performed)
    ############################################################################################################################################# REWORK THIS FUNCTION
    def __addPlatforms(self):
        uniqueGraphId = uuid.uuid1()
        name="NNCR"

        self.platforms.append({
            "id": uniqueGraphId,
        })

        self.platformsMapping[name] = uniqueGraphId

    ## Add sensors data to memory for graph creation
    ## Sensors define the sequencer used to get the sequencing data
    def __addSensors(self):
        for report in self.allReports:

            sensorName = self.__getValueFromColname(report["sections"][1]["data"][0], "Sequencing technology")

            if sensorName not in self.sensorsMapping.keys() and sensorName != "":
                uniqueGraphId = uuid.uuid1()

                self.sensors.append({
                    "id": uniqueGraphId,
                    "name": sensorName,
                    "isHostedBy": self.platformsMapping["NNCR"],
                })

                self.sensorsMapping[sensorName] = uniqueGraphId

    ## Add people data to memory for graph creation
    def __addPeople(self):
        for report in self.allReports:
            if report["sections"][0]["data"][0]["values"][10] not in self.peopleMapping.keys():
                uniqueGraphId = uuid.uuid1()
                name = report["sections"][0]["data"][0]["values"][10]
                email = ""
                
                ## some reports have different formats for the people data
                if len(report["sections"][0]["data"][0]["values"]) == 12:
                    email = report["sections"][0]["data"][0]["values"][11] 

                self.people.append({
                    "id": uniqueGraphId,
                    "name": name,
                    "email": email
                    })

                self.peopleMapping[name] = uniqueGraphId

    ## Add strains data to memory for graph creation
    ## feature to check if there is already an identical strain is missing in this function
    def __addStrains(self):
        for report in self.allReports:
            uniqueGraphId = uuid.uuid1()
            specieName = self.__getValueFromColname(report["sections"][2]["data"][0], "Isolate identified as")
            st = self.__getValueFromColname(report["sections"][2]["data"][0], "Sequence Type (ST)")
            if specieName in self.speciesTaxonomy:
                taxonomy = self.speciesTaxonomy[specieName]
            else:
                taxonomy = ""

            self.strains.append({
                "id": uniqueGraphId,
                "st": st,
                "taxonomy": taxonomy
            })

            self.strainsMapping[specieName] = uniqueGraphId 

    ## Add genes data to the memory for graph creation
    ## should get all the gene ontology id from the gene names to have fair data !
    ## TODO: Add the link with gene ontology
    def __addGenes(self):
        for report in self.allReports:
            for gene in report["sections"][3]["data"][0]["values"][0]:
                if gene not in self.genesMapping.keys():
                    uniqueGraphId = uuid.uuid1()
                    label = gene
                    if label in self.genesAroClasses:
                        aroClass = self.genesAroClasses[label]
                    else:
                        aroClass = ""

                    self.genes.append({
                        "id": uniqueGraphId,
                        "label": label, 
                        "aroClass": aroClass
                    })
                    self.genesMapping[label] = uniqueGraphId

    ## Adding all the observable properties used in the abromics reports in the 
    ## observableProperty list.
    def __addObservableProperties(self):
        for report in self.allReports:
            for observableProperty in report["sections"][3]["data"][0]["header"]: 
                if observableProperty not in self.observablePropertiesMapping.keys():
                    uniqueGraphId = uuid.uuid1()
                    label = observableProperty
                    self.observableProperties.append({
                        "id": uniqueGraphId,
                        "label": label
                    })
                    self.observablePropertiesMapping[label] = uniqueGraphId

    ## Add the samples data to memory for graph creation
    def __addSamples(self):
        for report in self.allReports:
            abromicsId = self.__getValueFromColname(report["sections"][1]["data"][0], "ABRomics ID")
            if abromicsId == None or abromicsId == "":
                continue
            if abromicsId not in self.samplesMapping.keys():
                uniqueGraphId = uuid.uuid1()
                countryName = self.__getValueFromColname(report["sections"][1]["data"][0], "Country")
                collectionDate = self.__getValueFromColname(report["sections"][1]["data"][0], "Collection date")
                if collectionDate != "":
                    try:
                        collectionDate = parser.parse(collectionDate)
                    except:
                        collectionDate = parser.parse("1970-01-01") ## In case of an error, just use the default collectionDate value
                else:
                    collectionDate = parser.parse("1970-01-01")
                
                print(f"collection date: {collectionDate}")
                if datetime.strftime(collectionDate, "%Y"):
                    collectionDate = datetime.strftime(collectionDate, '%Y-01-01')
                print(f"real collection date: {collectionDate}")

                microorganism = self.__getValueFromColname(report["sections"][2]["data"][0], "Isolate identified as")

                host = self.__getValueFromColname(report["sections"][1]["data"][0], "Host")
                
                sampleType = self.__getValueFromColname(report["sections"][1]["data"][0], "Sample type")
                sampleSource = self.__getValueFromColname(report["sections"][1]["data"][0], "Sample source")
                sensor = self.__getValueFromColname(report["sections"][1]["data"][0], "Sequencing technology")

                self.samples.append({
                    "id": uniqueGraphId,
                    "originalSampleId": abromicsId,
                    "strainId": report["sections"][1]["data"][0]["values"][1],
                    "microorganism": self.speciesTaxonomy[microorganism] if microorganism in self.speciesTaxonomy.keys() else "",
                    "collectionDate": collectionDate,
                    "sampleType": sampleType,
                    "sampleSource": self.sampleSourcesBindNCIT[sampleSource] if sampleSource in self.sampleSourcesBindNCIT.keys() else "", ## BUG # always return en empty string
                    "host": self.speciesTaxonomy[host] if host in self.speciesTaxonomy.keys() else "",
                    "country": self.countries[countryName] if countryName in self.countries.keys() else "",
                    "sequencingTechnology": self.sensorsMapping[sensor] if sensor in self.sensorsMapping.keys() else ""
                })

                ## self.samplesSubmitters[originalSampleId] = submitterId
                self.samplesMapping[abromicsId] = uniqueGraphId


    ## Add the observations made on all the samples
    ########################################################################################################################################### NOT FINISHED - HERE ##
    ## TODO: Add the madeby sensor, used procedure and hasResult fields to the ttl observation file
    def __addObservations(self):
        reportId = 0
        observationHeaderId = 0
        observationId = 0
        for report in self.allReports:
            for observationHeader in report["sections"][3]["data"][0]["header"]:
                for observation in report["sections"][3]["data"][0]["values"][observationHeaderId]:
                    uniqueGraphId = uuid.uuid1()
                    
                    abromicsId = self.__getValueFromColname(report["sections"][1]["data"][0], "ABRomics ID") ## The samplesMapping is empty old abromics reports have an other key for hte ABRomics ID and it's not in the right place in the reports. 
                    sampleFeatureOfInterest = self.samplesMapping[abromicsId]
                    geneFeatureOfInterest = self.genesMapping[report["sections"][3]["data"][0]["values"][0][observationId]]
                    observableProperty = self.observablePropertiesMapping[observationHeader]

                    sensorName = self.__getValueFromColname(report["sections"][1]["data"][0], "Sequencing technology")
                    sensor = "" if sensorName == "" else self.sensorsMapping[sensorName]
                    procedure = self.proceduresMapping["workflow 1 (genomic)"]

                    resultTime = self.__getValueFromColname(report["sections"][1]["data"][0], "Collection date")
                    try:
                        resultTime = parser.parse(resultTime)
                    except:
                        resultTime = parser.parse("1970-01-01")
                    if datetime.strftime(resultTime, "%Y"):
                        resultTime = datetime.strftime(resultTime, '%Y-01-01')

                    self.observations.append({
                        "id": uniqueGraphId,
                        "sample": sampleFeatureOfInterest, ## legacy (no longer used but may be interesting with the changes in sosa ontolgy 
                        "gene": geneFeatureOfInterest,
                        "observableProperty": observableProperty,
                        "sensor": sensor,
                        "procedure": procedure,
                        "simpleResult": observation,
                        "resultTime": resultTime
                    })

                    observationId = observationId + 1 
                observationId = 0
                observationHeaderId = observationHeaderId + 1
            observationHeaderId = 0
            reportId = reportId + 1


    ## Add the links between the samples and the observations in a variable that will be used in 
    ## the links_samples_observations.j2 jinja template
    ## This function is very very inefficient.. but I had not enough time to make it efficient
    def __addLinksSamplesObservations(self):
        for observation in self.observations:
            self.linksSamplesObservations.append({
                "sample": observation["sample"],
                "observation": observation["id"]
            })

    ## Create and send a sparql query that will generate the knowledge graph in a graph server
    def __UploadGraphToServer(self):
        ## Try to create the abromics data graph 
        create_graph_query = "CREATE GRAPH <http://data.abromics.fr>"
        print("creating the abromics data graph")
        print(create_graph_query)
        sparql = SPARQLWrapper(self.sparqlEndpoint)
        sparql.setReturnFormat(JSON)
        sparql.setQuery(create_graph_query)
        try:
            res = sparql.query().convert()
            recs = res["results"]["bindings"]
        except Exception as e: 
            print(e) ## When there is an error here it means that the graph already exists
        
        ## Craft the add nodes from rdf files sparql queries
        with open(f"{outputPath}/genes.ttl") as file:
            query = "INSERT DATA { GRAPH <http://data.abromics.fr> { "
            for line in file:
                if line[0] != "@":
                    query = query + str(line)
            query = query + "}}"
            #with open(f"test.sparql", "w") as test:
            #    test.write(query)

        ## Execute the sparql queries
        print("Executing the data addition queries")
        print(query)
        sparql = SPARQLWrapper(self.sparqlEndpoint)
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query)
        try:
            res = sparql.query().convert()
            recs = res["results"]["bindings"]
        except Exception as e: 
            print(e) 


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

    def createGraph(self, fetchCountriesFromCache = None, templatePath = "", outputPath = ""):

        ## Loading the reports in memory
        if len(self.reportDirectories) != 0:
            for reportDirectory in self.reportDirectories:
                self.allReports.extend([self.__readJsonFromFile(f"{reportDirectory}/{reportFilename}") for reportFilename in os.listdir(reportDirectory) if reportFilename.endswith(".json")])
        else:
            print("no input report directory indicated. Give a list of report directories to use as input for the graph creation process")
            exit()

        ## Curate the reports
        self.__curateReports()

        ## Ask the user when the way to get the countries is not indicated
        if fetchCountriesFromCache is None: 
            choiceCountries = input("Get fresh countries data (from wikidata) ? [yes/no] ")
            if choiceCountries == "yes": 
                self.__getCountries(from_cache=False)
            else:
                self.__getCountries(from_cache=True)
        else:
            self.__getCountries(from_cache=fetchCountriesFromCache)

        self.__getSpeciesTaxonomy()
        self.__getSampleSources()
        self.__getAroClasses()

        ## Adding entity data in memory 
        self.__addPlatforms()
        self.__addSensors()
        self.__addProcedures()
        ## self.__addPeople() ## People associated with the report is no longer available in the new versions of the ABRomics reports
        self.__addStrains()
        self.__addObservableProperties() 
        self.__addGenes()
        self.__addSamples()
        self.__addObservations()

        ## Add many to many links
        self.__addLinksSamplesObservations()

        ## Creating the turtle file
        self.__createTtlFile(f"{templatePath}platforms.j2", outputPath, "platforms", self.platforms) 
        self.__createTtlFile(f"{templatePath}sensors.j2", outputPath, "sensors", self.sensors) 
        self.__createTtlFile(f"{templatePath}procedures.j2", outputPath, "procedures", self.procedures) 
        ## self.__createTtlFile(f"{templatePath}graph-templates/people.j2", outputPath, "people", self.people) 
        self.__createTtlFile(f"{templatePath}strains.j2", outputPath, "strains", self.strains)
        self.__createTtlFile(f"{templatePath}observable-properties.j2", outputPath, "observableProperties", self.observableProperties)
        self.__createTtlFile(f"{templatePath}genes.j2", outputPath, "genes", self.genes)
        self.__createTtlFile(f"{templatePath}samples.j2", outputPath, "samples", self.samples, filterFunctions=[{"name": "isDatetime", "content": self.__isDatetime}])
        self.__createTtlFile(f"{templatePath}observations.j2", outputPath, "observations", self.observations, filterFunctions=[{"name": "isFloat", "content": self.__isFloat}])
        self.__createTtlFile(f"{templatePath}links_samples_observations.j2", outputPath, "linksSamplesObservations", self.linksSamplesObservations)

        


if __name__ == "__main__":
    print("=== Graph creator module ===\n")
    reportsDirs = ["../graph_downloader/uc1-reports", "../graph_downloader/uc2-reports"]
    outputPath = "out"
    choiceCreateNewGraph = input(f"\nCreate new graph (this action is destructive) (deleted content: {outputPath}/) ? [yes/no] ")
    if choiceCreateNewGraph == "yes": 
        gc = GraphCreator(reportDirectories=reportsDirs, cacheDirectory="cache")
        gc.createGraph(templatePath="graph-templates/", outputPath=outputPath)
