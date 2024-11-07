
from alive_progress import alive_bar
import time
import requests
import os
import json
from dotenv import load_dotenv


## Downloader class allows to fetch abromics reports from the api, filter them 
## and save them locally
class Downloader():

    def __init__(self):

        ## env variables (get the user ABRomics credentials from .env file)
        load_dotenv()
        
        ## load the environment variables
        self.api_url = "https://analysis.abromics.fr" # os.getenv('API_URL') 
        self.email = ""
        self.password = ""
        self.api_user_token = "YWRtaW5AYW5hbHlzaXMuYWJyb21pY3MuZnI6YWJyb21pY3MyMDIz" # This is the master basic token # os.getenv('API_USER_TOKEN')

    ## Public methods

    def getUserToken(self):
        response = requests.post(
            "https://analysis.abromics.fr/api/login", 
            data={
                "email": self.email, 
                "password": self.password
            }
        )
        try:
            response = response.json()
        except:
            print(f"Invalid Credentials: {response}")
            exit()
        self.api_user_token = response.access

    ## download all the abromics reports marked as "ready to report" 
    ## downloadDir (string) : indicate the directory in which the reports should be saved
    def getAllAbromicsReadyReports(self, downloadDir):
        response = { "next": "https://analysis.abromics.fr/api/analysis/" }
        exploitable_analysis_ids = []
        while "next" in response and response["next"] != None: 
            response = requests.get(
                response["next"],
                params={'status': 'ready_to_report'},
                headers = {
                    'Authorization': f"Basic {self.api_user_token}", ## replace Basic with Bearer if it's a Bearer token
                }
            )
            response = response.json()
            ## print(response)
            for analysis in response["results"]:
                exploitable_analysis_ids.append(analysis["id"])

        print(f"{len(exploitable_analysis_ids)} reports will be downloaded ...")

        if not os.path.exists(downloadDir):
            os.makedirs(downloadDir)
    
        with alive_bar(len(exploitable_analysis_ids)) as bar:
            countDownloadFails = 0
            countDownloadSuccess = 0
            for report_id in exploitable_analysis_ids:
                print(report_id)
                response = requests.get(
                    f"https://analysis.abromics.fr/api/analysis/{report_id}/report/",
                    headers = {
                        'Authorization': f"Basic {self.api_user_token}", ## replace Basic with Bearer if it's a Bearer token
                    }
                )
                try:
                    report = response.json()
                    # save the reports in a local file
                    with open(f'{downloadDir}/abr_report_{report_id}.json', 'w') as f:
                        json.dump(report, f)
                    countDownloadSuccess += 1
                except:
                    print("report not downloaded - Wrong format")
                    countDownloadFails += 1
                bar()
            print(f"Download finish ! \nnb success: {countDownloadSuccess}\nnb fails: {countDownloadFails}")


## Download all the abromics reports marked as ready to report
downloadDir = "reports"
choiceDownloadFreshReports = input(f"Download fresh reports data from abromics (this action is destructive) (target directory: {downloadDir}) ? [yes/no] ")
if choiceDownloadFreshReports == "yes": 
    downloader = Downloader()
    downloader.getAllAbromicsReadyReports(downloadDir)

