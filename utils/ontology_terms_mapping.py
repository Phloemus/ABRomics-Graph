import json
import os
from SPARQLWrapper import SPARQLWrapper, JSON


def readJsonFromFile(path):
    with open(path) as f:
        d = json.load(f)
        return d

filePath = input("The path of the json file containing the terms you want to map on the onotologies: ")
data = readJsonFromFile(filePath)

allTermsList = list()
allTermsString = ""
for item in data:
    value = item['fields']['name']
    if value not in allTermsList:
        allTermsList.append(value)
        allTermsString += f"'{value}' "
print(allTermsString)
sparql_query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?class ?classLabel WHERE {{
        VALUES ?classLabel {{ 
            {allTermsString}
        }}
        ?class rdfs:label ?classLabel .
    }}
"""
print("Fetching sample source classes ...")
sparql = SPARQLWrapper("https://10-54-3-233.gcp.glicid.fr/sparql")
sparql.setReturnFormat(JSON)
sparql.setQuery(sparql_query)
try:
    res = sparql.query().convert()
    recs = res["results"]["bindings"]
    
    output = data
    count = 0
    success = 0
    for item in data:
        value = item["fields"]["name"]
        for res in recs:
            if value == res["classLabel"]["value"]:
                output[count]["fields"]["class"] = res["class"]["value"]
                success = success + 1
        count = count + 1

    json_str = json.dumps(output, indent=4)
    with open("sources-with-ontology-terms.json", "w") as f:
        f.write(json_str)
    print(f"number of found classes: {success} on {count}")
except Exception as e:
    print(e)



