from alive_progress import alive_bar
import requests
import os
import json
from dotenv import load_dotenv
from getpass4 import getpass
import shutil
import xmltodict
import xml.etree.ElementTree as ET
import json
import pandas as pd
import time

## Downloader class allows to fetch abromics reports from the api, filter them 
## and save them locally
class Downloader():

    def __init__(self, downloadDir = ".", email = "", password = ""):

        ## env variables (get the user ABRomics credentials from .env file)
        load_dotenv()
        
        ## load the environment variables
        self.api_url = "https://analysis.abromics.fr" # os.getenv('API_URL') 
        self.email = email
        self.password = password
        self.api_user_access_token = ""
        self.api_user_refresh_token = ""
        self.downloadDir = downloadDir

    ## Public methods

    ## Method used for manual authentification
    def authenticate(self):

        email = self.email
        password = self.password

        if self.email == "" or self.password == "":
            print("User authenfication")
            email = input("Enter your email: ")
            password = getpass("Password: ")

        response = requests.post(
            "https://analysis.abromics.fr/api/login/", 
            json={
                "email": email,
                "password": password
            }
        )
        try:
            response.raise_for_status()
            response = response.json()
            self.api_user_access_token = response['access']
            self.api_user_refresh_token = response['refresh']
        except requests.exceptions.HTTPError as e:
            print(e)
            exit()


    ## Used to get a fresh access token from the refresh access token given 
    ## during the authentification process
    def refreshAccessToken(self):
        response = requests.post(
            "https://analysis.abromics.fr/api/token/refresh/", 
            json={
                "refresh": self.api_user_refresh_token
            }
        )
        try:
            response.raise_for_status()
            response = response.json()
            self.api_user_access_token = response['access']
        except requests.exceptions.HTTPError as e:
            print(e)
            exit()

    ## Transform geospacial string coordinates from this format "N16.3 E20.71" to latitude, logitude coordinates
    def parseLatLon(self, coord_str):
        lat_str, lat_dir, lon_str, lon_dir = coord_str.split()
        lat, lon = float(lat_str), float(lon_str)
        if lat_dir.upper() == "S": lat = -lat
        if lon_dir.upper() == "W": lon = -lon
        return lat, lon
    
    def getAllSRAIdsFromSRR(self, srr):
        base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
        # Search SRR in SRA database
        search_url = f"{base}esearch.fcgi"
        params = {
            "db": "sra",
            "term": srr,
            "retmode": "json"
        }
    
        r = requests.get(search_url, params=params)
        data = r.json()
    
        if not data["esearchresult"]["idlist"]:
            print("SRR not found")
            return None
    
        sra_id = data["esearchresult"]["idlist"][0]

        # Fetch full metadata XML
        fetch_url = f"{base}efetch.fcgi"
        params = {
            "db": "sra",
            "id": sra_id,
            "retmode": "xml"
        }
    
        r = requests.get(fetch_url, params=params)
        root = ET.fromstring(r.content)

        # Extract accessions
        srx = root.find(".//EXPERIMENT").attrib.get("accession")
        prjna = root.find(".//STUDY").attrib.get("accession")

        # Correct way to get SAMN
        samn = None
        for ext_id in root.findall(".//EXTERNAL_ID"):
            if ext_id.attrib.get("namespace") == "BioSample":
                samn = ext_id.text
                break

        return {
            "SRR": srr,
            "SRX": srx,
            "SAMN": samn,
            "PRJNA ": prjna
        }

    def getPublicReportsFromWorkflowResult(self, workflowOutputFilePath):
        df = pd.read_csv(workflowOutputFilePath, sep="\t")
        df["SRR"] = df["Contig"].str.split("_").str[0]
        unique_srr = df["SRR"].dropna().unique().tolist()

        print(f"{len(unique_srr)} unique SRR found in {workflowOutputFilePath}")

        with alive_bar(len(unique_srr)) as bar:
            srr_results = {}
            for srr in unique_srr:
                metadata = self.getAllSRAIdsFromSRR(srr)
                srr_results[srr] = metadata
                time.sleep(0.4)   # Respect NCBI rate limit (3 req/sec)
                bar()

        ncbiIdsDf = pd.DataFrame.from_dict(srr_results, orient="index")

        df = df.merge(ncbiIdsDf, on="SRR", how="left")

        ## Get the sample metadata in the df
        unique_samn = df["SAMN"].dropna().unique().tolist()

        print(f"{len(unique_srr)} unique SAMN found")
        print("Getting the biosample metadata from NCBI")

        with alive_bar(len(unique_samn)) as bar:
            samn_results = {}
            for samn in unique_samn:
                url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=biosample&id={samn}&retmode=xml"
                response = requests.get(url)
                samn_metadata = xmltodict.parse(response.text)
                biosampleMetadata = samn_metadata['BioSampleSet']['BioSample']
                collectionDate = ""
                country = ""
                city = ""
                latitude = 0
                longitude = 0
                for attribute in biosampleMetadata['Attributes']['Attribute']:
                    if attribute['@attribute_name'] == "collection_date":
                        collectionDate = attribute['#text']
                    if attribute['@attribute_name'] == "geo_loc_name":
                        country = attribute['#text'].split(":")[0]
                        city = attribute['#text'].split(":")[1]
                        city = city.lstrip(" ")
                    if attribute['@attribute_name'] == "lat_lon":
                        latitude, longitude = self.parseLatLon(attribute['#text'])
                samn_results[samn] = {
                    "SAMN": samn,
                    "ABRomics ID": samn, 
                    "Microorganism scientific name": "", 
                    "Collection date": collectionDate,
                    "Sample type": "environmental",
                    "Sample source": "WWTP effluant",
                    "Host": "",
                    "Country": country,
                    "City": city,
                    "Latitude": latitude,
                    "Longitude": longitude,
                    "Sequencing technology": ""
                }
                time.sleep(0.4)   # Respect NCBI rate limit (3 req/sec)
                bar()

        samnMetadataDf = pd.DataFrame.from_dict(samn_results, orient="index")

        df = df.merge(samnMetadataDf, on="SAMN", how="left")

        ## Generate the sample metadata section of the report
        print("Generating the analysis reports")
        reportsCounter = 0
        samplesDf = df.drop_duplicates(subset=["SAMN"], keep="first")
        with alive_bar(len(samplesDf)) as bar:
            for index, sample in samplesDf.iterrows():
                titleSection = {"title": "GALAXY METAGENOMIC WORKFLOW RESULT REPORT"}
                sampleMetadataSection = {"data": [
                    {
                        "type": "summary",
                        "header": ["ABRomics ID", "Microorganism scientific name", "Collection date", "Sample type", "Sample source", "Host", "Country", "City", "Latitude", "Longitude", "Sequencing technology"],
                        "values": [sample["ABRomics ID"], "", sample["Collection date"], "environmental", "WWTP effluant", "", sample["Country"], sample["City"], sample["Latitude"], sample["Longitude"], ""]
                    }
                ]}
                sampleTaxonomyAndStSection = {"data": [
                    {
                        "type": "summary", 
                        "header": ["Isolate identified as", "Sequence Type (ST)", "Number of genes with known resistance to target antibiotics"],
                        "values": ["", "", ""]
                    }
                ]}
                sampleObservationsDf = df[df["SAMN"] == sample["SAMN"]]
                resistanceGenes = []
                geneLengths = []
                identityPercentages = []
                overlapPercentages = []
                contigs = []
                startInContigs = []
                endInContigs = []
                strands = []
                targetAntibiotics = [] 
                accessionNumbers = []
                for index, observation in sampleObservationsDf.iterrows():
                    resistanceGenes.append(observation['Gene'])
                    geneLengths.append(observation['HSP Length/Total Length'].split("/")[0]) 
                    identityPercentages.append(observation['%Identity'])
                    overlapPercentages.append(observation['%Overlap'])
                    contigs.append(observation['Contig'])
                    startInContigs.append(observation['Start'])
                    endInContigs.append(observation['End'])
                    for antibiotic in observation['Predicted Phenotype'].split(","):
                        if antibiotic not in targetAntibiotics:
                            targetAntibiotics.append(antibiotic.strip())
                    accessionNumbers.append(observation['Accession'])
                sampleObservationsSection = {"data": [
                    {
                        "type": "data-table", 
                        "header": ["Resistance gene", "Gene length", "Identity (%)", "Overlap (%)", "Contig", "Start in contig", "End in contig", "Target antibiotic", "# Accession"],
                        "values": [resistanceGenes, geneLengths, identityPercentages, overlapPercentages, contigs, startInContigs, endInContigs, targetAntibiotics, accessionNumbers]
                    }
                ]}

                sections = [titleSection, sampleMetadataSection, sampleTaxonomyAndStSection, sampleObservationsSection]

                reportDict = {
                    "title": "GALAXY METAGENOMIC WORKFLOW RESULT REPORT",
                    "sections": sections,
                }

                with open(f"{self.downloadDir}/custom_abr_report_{sample['SAMN']}.json", 'w') as f:
                    json.dump(reportDict, f, indent=2)
                reportsCounter += 1
                bar()
        print(f"{reportsCounter} reports from public samples generated")


    ## download all the abromics reports marked as "ready to report" 
    ## downloadDir (string) : indicate the directory in which the reports should be saved
    def getAllAbromicsReadyReports(self):
        response = { "next": "https://analysis.abromics.fr/api/analysis/?status=ready_to_report" }
        exploitable_analysis_ids = []
        while "next" in response and response["next"] != None: 
            print(response["next"])
            response = requests.get(
                response["next"], ## ?status=ready_to_report is auto integrated in the next url responded by ABRomics
                headers = {
                    'Authorization': f"Bearer {self.api_user_access_token}", ## replace Basic with Bearer if it's a Bearer token
                }
            )
            response = response.json()
            for analysis in response["results"]:
                exploitable_analysis_ids.append(analysis["id"])

        print(f"{len(exploitable_analysis_ids)} reports will be downloaded ...")

        if not os.path.exists(self.downloadDir):
            os.makedirs(self.downloadDir)
    
        with alive_bar(len(exploitable_analysis_ids)) as bar:
            countDownloadFails = 0
            countDownloadSuccess = 0
            countTotal = 0
            for report_id in exploitable_analysis_ids:
                print(report_id)
                response = requests.get(
                    f"https://analysis.abromics.fr/api/analysis/{report_id}/report/",
                    headers = {
                        'Authorization': f"Bearer {self.api_user_access_token}", ## replace Basic with Bearer if it's a Bearer token
                    }
                )
                if response.status_code == 401:
                    print(f"token expired.. retrying downloading report {report_id}")
                    self.refreshAccessToken()
                    response = requests.get(
                        f"https://analysis.abromics.fr/api/analysis/{report_id}/report/",
                        headers = {
                            'Authorization': f"Bearer {self.api_user_access_token}", ## replace Basic with Bearer if it's a Bearer token
                        }
                    )
                try:
                    report = response.json()
                    print(report)
                    # save the reports in a local file
                    with open(f'{self.downloadDir}/abr_report_{report_id}.json', 'w') as f:
                        json.dump(report, f)
                    countDownloadSuccess += 1
                except Exception as e:
                    print(f"report not downloaded - Exception: {e}")
                    countDownloadFails += 1
                bar()
            print(f"Download finish ! \nnb success: {countDownloadSuccess}\nnb fails: {countDownloadFails}")


## Used to curate downloaded reports using values present in the reports. 
## Like filtering the reports depending on the country etc
## This class allows to copy the some reports over to an other directory
class ReportCurator():

    def __init__(self, allReportsPath= ".", curatorOutputPath= "", metadataFilters={}):
        self.allReportsPath = allReportsPath
        self.curatorOutputPath = curatorOutputPath
        self.metadataFilters = metadataFilters
        self.allReportsFilenames = []
        self.allReports = [self.__readJsonFromFile(f"{allReportsPath}/{reportFilename}", reportFilename) for reportFilename in os.listdir(allReportsPath) if reportFilename.endswith(".json")]
        self.curatedReportsFilenames = []

        if not os.path.exists(self.curatorOutputPath):
            os.makedirs(self.curatorOutputPath)


    def __getValueFromColname(self, tableData, label):
        if len([id for id, value in enumerate(tableData["header"]) if value == label]) != 0: 
            headerId = [id for id, value in enumerate(tableData["header"]) if value == label][0]
            if headerId != None:
                return tableData["values"][headerId]
            else: 
                return ""
        else:
            return ""

    def __readJsonFromFile(self, path, filename):
        with open(path) as f:
            d = json.load(f)
            self.allReportsFilenames.append(filename)
            return d

    ## curate the reports by only copying the reports have enough metadata and metadata that match the constraints given by the metadata filters
    ##! verify that the curation for uc1 is working correctly
    ##! check if it works for the reports of uc3
    def curateReports(self):
        self.curatedReportsFilenames = []
        i = 0
        for report in self.allReports:
            i += 1
            isMetadataOk = False
            for key, value in self.metadataFilters.items():
                inReportMetadataValue = self.__getValueFromColname(report["sections"][1]["data"][0], key)
                if inReportMetadataValue != "" and (inReportMetadataValue == value or value == "*"):
                    isMetadataOk = True
            if isMetadataOk:
                self.curatedReportsFilenames.append(self.allReportsFilenames[i-1])
                shutil.copy(f"{self.allReportsPath}/{self.allReportsFilenames[i-1]}", f"{self.curatorOutputPath}/{self.allReportsFilenames[i-1]}")
        print(f"{len(self.curatedReportsFilenames)}/{len(self.allReportsFilenames)} reports kept after curation with given metadata filters")




if __name__ == "__main__":
    choiceOption = input(f"Report downloader module\n\n1.Download reports (UC1, UC2, UC3)\n2.Curate UC1, UC2, UC3 reports\n\nSelect an option (1 or 2)\n")
    if choiceOption == "1":
        downloadDir = "reports"
        choiceDownloadFreshReports = input(f"Download fresh reports data from abromics (this action is destructive) (targeted directory: {downloadDir}) ? [yes/no] ")
        if choiceDownloadFreshReports == "yes": 
            downloader = Downloader(downloadDir = downloadDir)
            print("\n=== Public reports ===\nDownloading and creating reports based on publicly available samples in NCBI")
            downloader.getPublicReportsFromWorkflowResult("resfinder-galaxy-results.tsv")
            print("\n=== Private reports ===\nDownloading reports from the ABRomics database. Needs an authentification using ABRomics credentials (https://analysis.abromics.fr/register)")
            downloader.authenticate()
            print("Preparing the downloading process can be a bit long. Please wait..")
            downloader.getAllAbromicsReadyReports()

    if choiceOption == "2":
        choiceCurateReports = input(f"Curation of the uc1 and uc2 reports (this action is destructive) (targeted directories: uc1-reports and uc2-reports) ? [yes/no] ")
        if choiceCurateReports == "yes":
            uc1Curator = ReportCurator("reports", "uc1-reports", {"Submitter name": "Claudine Médigue"})
            uc1Curator.curateReports()
            uc2Curator = ReportCurator("reports", "uc2-reports", {"Country": "Chile"})
            uc2Curator.curateReports()
            uc3Curator = ReportCurator("reports", "uc3-reports", {"Longitude": "*"})
            uc3Curator.curateReports()