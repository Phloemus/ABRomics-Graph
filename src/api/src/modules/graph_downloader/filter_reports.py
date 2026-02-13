import os
import json
import requests
import shutil

def readJsonFromFile(path, filename, allReportsFilenames):
    with open(path) as f:
        d = json.load(f)
        allReportsFilenames.append(filename)
        return d

## curate the reports and only keep the reports that contains all the required fields
def curateReports(allReports, allReportsFilenames):
    curatedReports = []
    curatedReportsFilenames = []
    i = 0
    for report in allReports:
        i += 1
        if len(report["sections"][0]["data"][0]["values"]) < 11:
            continue
        curatedReports.append(report)
        curatedReportsFilenames.append(allReportsFilenames[i-1])
    return {"reports": curatedReports, "reportsFilenames": curatedReportsFilenames}


allReportsFilenames = []
allReports = []
allReports = [readJsonFromFile(f"reports/{reportFilename}", reportFilename, allReportsFilenames) for reportFilename in os.listdir("reports") if reportFilename.endswith(".json")]

data = curateReports(allReports, allReportsFilenames)
allReports = data["reports"]
allReportsFilenames = data["reportsFilenames"]

accessToken = ""


def authenticate():
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
        accessToken = response['access']
    except requests.exceptions.HTTPError as e:
        print(e)
        exit()


def getPublicReportsIds():
    response = { "next": "https://analysis.abromics.fr/api/report" }
    publicReportIds = []
    while "next" in response and response["next"] != None:
        response = requests.get(
            response["next"],
            params={'status': 'ready_to_report'},
            headers = {
                'Authorization': f"Bearer {accessToken}"
            }
         )
        try:
            response = response.json()
            for report in response["results"]:
                publicReportIds.append(report["id"])
        except:
            print("miswritten json string")
    return publicReportIds

# publicReportIds = getPublicReportsIds()
# print(publicReportIds)


## Filter only the reports made by Claudine and the sampleId has to be exaclty the same as one that is present in the public database of ABRomics
nbReportsPublishable = 0
nbReportsNotPublishable = 0
i = 0
for report in allReports:
    if report["sections"][0]["data"][0]["values"][10] == "Claudine Médigue":
        shutil.copy(f"reports/{allReportsFilenames[i]}", f"reports-claudine/{allReportsFilenames[i]}")
        nbReportsPublishable += 1
    else:
        nbReportsNotPublishable += 1
    i += 1

print(f"Filtration finished !\nnb publishable: {nbReportsPublishable}\nnb not publishable: {nbReportsNotPublishable}")


