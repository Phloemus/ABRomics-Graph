
import os
import glob
import shutil
import pytest
import requests
from getpass4 import getpass

from routes.abromics import getSampleSources
from utils.query import Query
from config.constants import QUERIES 
from config.config import SPARQL_ENDPOINT

from modules.graph_downloader.graph_downloader import Downloader
from modules.graph_creator.graph_creator import GraphCreator


queryPathPrefix = "../src"
temporaryPath = "./temp"

print("\n\nSome of these tests need a connection to the ABRomics plateform")
email = input("Enter your email: ")
password = getpass("Password: ")


"""
    Should connect to the sparql endpoint and returning a valid status code
"""
def test_sparql_endpoint_activity():
    try:
        r = requests.get(SPARQL_ENDPOINT)
    except Exception as e:
        assert False
    assert r.status_code == 200


"""
    Should check if the samples source of humans are accessible via the 
    knowledge graph
"""
def test_human_sample_sources():
    query = Query(f"{queryPathPrefix}/{QUERIES[5]['filePath']['animal']}", sparqlEndpoint=SPARQL_ENDPOINT, parameters={"specieName": "Homo sapiens" })
    res = query.executeQuery()
    assert "status" not in res or res["status"] == "error"


"""
    Should check if the samples source for an animal are accessible via the 
    knowledge graph
"""
def test_animal_sample_sources(): 
    query = Query(f"{queryPathPrefix}/{QUERIES[5]['filePath']['animal']}", sparqlEndpoint=SPARQL_ENDPOINT, parameters={"specieName": "Mus musculus" })
    res = query.executeQuery()
    assert "status" not in res or res["status"] == "error"


def test_animal_no_specie_sample_sources(): 
    query = Query(f"{queryPathPrefix}/{QUERIES[5]['filePath']['animal']}", sparqlEndpoint=SPARQL_ENDPOINT)
    res = query.executeQuery()
    assert "status" not in res or res["status"] == "error"


def test_environmental_sample_sources(): 
    query = Query(f"{queryPathPrefix}/{QUERIES[5]['filePath']['environmental']}", sparqlEndpoint=SPARQL_ENDPOINT)
    res = query.executeQuery()
    assert "status" not in res or res["status"] == "error"


def test_all_sample_sources(): 
    query = Query(f"{queryPathPrefix}/{QUERIES[5]['filePath']['all']}", sparqlEndpoint=SPARQL_ENDPOINT)
    res = query.executeQuery()
    assert "status" not in res or res["status"] == "error"



## Test get all the abromics reports
def testDownladReports():
    downloader = Downloader(downloadDir = f"{temporaryPath}/reports", email = email, password = password)
    downloader.authenticate()
    print("Wait for downloading process to be launched..")
    downloader.getAllAbromicsReadyReports()
    assert os.path.exists(glob.glob(f"{temporaryPath}/reports/*.json")[0]) == True


## Test of the graph creation
def testGraphCreation():
    gc = GraphCreator(reportDirectory = "temp/reports", sparqlEndpoint = "http://localhost:8890/sparql")
    gc.createGraph(fetchCountriesFromCache = False, templatePath = "src/modules/graph_creator/", outputPath="temp/graph_data")
    assert os.path.exists(glob.glob(f"{temporaryPath}/graph_data/*.ttl")[0]) == True
