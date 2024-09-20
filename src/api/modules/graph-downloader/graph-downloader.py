
from alive_progress import alive_bar
import time
import requests


## Downloader class allows to fetch abromics reports from the api, filter them 
## and save them locally
class Downloader():

    def __init__(self):

        ## env variables (get the user ABRomics credentials from .env file)
        load_dotenv()
        
        ## load the environment variables
        self.api_url = os.getenv('API_URL') 
        self.api_username = os.getenv('API_USERNAME')
        self.api_password = os.getenv('API_PASSWORD')
        self.api_temp_basic_token = os.getenv('API_TEMP_BASIC_TOKEN')

    ## Public methods

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
                    'Authorization': f"Basic {self.api_temp_basic_token}",
                }
            )
            response = response.json()
            for analysis in response["results"]:
                exploitable_analysis_ids.append(analysis["id"])

        print(f"{len(exploitable_analysis_ids)} reports will be downloaded ...")

        if not os.path.exists(downloadDir):
            os.makedirs(downloadDir)
    
        with alive_bar(len(exploitable_analysis_ids)) as bar:
            for report_id in exploitable_analysis_ids:
                print(report_id)
                response = requests.get(
                    f"https://analysis.abromics.fr/api/analysis/{report_id}/report/",
                    headers = {
                        'Authorization': f"Basic {self.api_temp_basic_token}",
                    }
                )
                report = response.json()
                
                # save the reports in a local file
                with open(f'{downloadDir}/abr_report_{report_id}.json', 'w') as f:
                    json.dump(report, f)
                bar()



## Download all the abromics reports marked as ready to report
downloadDir = "reports"
choiceDownloadFreshReports = input(f"Download fresh reports data from abromics (this action is destructive) (target directory: {downloadDir}) ? [yes/no] ")
if choiceDownloadFreshReports == "yes": 
    downloader = Downloader()
    downloader.getAllAbromicsReadyReports(downloadDir)

