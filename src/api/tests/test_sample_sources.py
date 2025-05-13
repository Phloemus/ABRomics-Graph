
import unittest
import requests

from routes.abromics import getSampleSources
from utils.query import Query
from config.constants import QUERIES 
from config.config import SPARQL_ENDPOINT

from modules.graph_downloader.graph_downloader import Downloader
from modules.graph_creator.graph_creator import GraphCreator

class TestSampleSource(unittest.TestCase):

    def setUp(self):
        self.queryPathPrefix = "../src"
        self.temporaryPath = "temp"
        pass


    def testSparqlEndpointActivity(self):
        try:
            r = requests.get(SPARQL_ENDPOINT)
        except Exception as e:
            self.assertTrue(False, "Should be able to connect to the sparql endpoint url")
        self.assertTrue(r.status_code == 200, "Should return a 200 status code")


    def testHumanSampleSources(self):
        query = Query(f"{self.queryPathPrefix}/{QUERIES[5]['filePath']['animal']}", sparqlEndpoint=SPARQL_ENDPOINT, parameters={"specieName": "Homo sapiens" })
        res = query.executeQuery()
        self.assertFalse("status" in res and res["status"] == "error", "Should return a query response as a json")


    def testAnimalSampleSources(self): 
        query = Query(f"{self.queryPathPrefix}/{QUERIES[5]['filePath']['animal']}", sparqlEndpoint=SPARQL_ENDPOINT, parameters={"specieName": "Mus musculus" })
        res = query.executeQuery()
        self.assertFalse("status" in res and res["status"] == "error", "Should return a query response as a json")


    def testAnimalNoSpecieSampleSources(self): 
        query = Query(f"{self.queryPathPrefix}/{QUERIES[5]['filePath']['animal']}", sparqlEndpoint=SPARQL_ENDPOINT)
        res = query.executeQuery()
        self.assertFalse("status" in res and res["status"] == "error", "Should return a query response as a json")


    def testEnvironmentalSampleSources(self): 
        query = Query(f"{self.queryPathPrefix}/{QUERIES[5]['filePath']['environmental']}", sparqlEndpoint=SPARQL_ENDPOINT)
        res = query.executeQuery()
        self.assertFalse("status" in res and res["status"] == "error", "Should return a query response as a json")


    def testAllSampleSources(self): 
        query = Query(f"{self.queryPathPrefix}/{QUERIES[5]['filePath']['all']}", sparqlEndpoint=SPARQL_ENDPOINT)
        res = query.executeQuery()
        self.assertFalse("status" in res and res["status"] == "error", "Should return a query response as a json")


    ## Test get all the abromics reports
    def testGetReports(self):
        downloader = Downloader()
        downloader.authenticate()
        downloader.getAllAbromicsReadyReports(f"{self.temporaryPath}/reports")

    ## Test of the graph creation
    ## def testGraphCreation(self):
    ##     gc = GraphCreator(reportDirectory = "temp/data/reports", sparqlEndpoint = "http://localhost:8890/sparql")
    ##     gc.createGraph(fetchCountriesFromCache = False, templatePath = "src/modules/graph_creator/", outputPath="temp/out")
        


if __name__ == "__main__":
    unittest.main()
