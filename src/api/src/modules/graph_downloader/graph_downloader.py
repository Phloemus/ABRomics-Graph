from alive_progress import alive_bar
import time
import requests
import os
import json
from dotenv import load_dotenv
from getpass4 import getpass
import shutil


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
    def curateReports(self):
        self.curatedReportsFilenames = []
        i = 0
        for report in self.allReports:
            i += 1
            isMetadataOk = False
            if len(report["sections"][1]["data"][0]["values"]) < 7:
                continue
            for key, value in self.metadataFilters.items():
                inReportMetadataValue = self.__getValueFromColname(report["sections"][1]["data"][0], key)
                print(f"{inReportMetadataValue} - {value}")
                if inReportMetadataValue != None and inReportMetadataValue == value:
                    isMetadataOk = True
            if isMetadataOk:
                self.curatedReportsFilenames.append(self.allReportsFilenames[i-1])
                shutil.copy(f"{self.allReportsPath}/{self.allReportsFilenames[i-1]}", f"{self.curatorOutputPath}/{self.allReportsFilenames[i-1]}")
        print(f"{len(self.curatedReportsFilenames)}/{len(self.allReportsFilenames)} reports kept after curation with given metadata filters")




if __name__ == "__main__":
    choiceOption = input(f"Report downloader module\n\n1.Download reports\n2.Curate UC1 and UC2 reports\n\nSelect an option (1 or 2)\n")
    if choiceOption == "1":
        downloadDir = "reports"
        choiceDownloadFreshReports = input(f"Download fresh reports data from abromics (this action is destructive) (targeted directory: {downloadDir}) ? [yes/no] ")
        if choiceDownloadFreshReports == "yes": 
            downloader = Downloader(downloadDir = downloadDir)
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