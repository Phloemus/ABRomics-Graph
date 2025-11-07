import json

def readJson(filename):
    ontologies = {}
    with open(filename, 'r') as file:
        data = json.load(file)
        for item in data:
            if "FOODON" in item["fields"]["class"]:
                item["fields"]["ontology"] = "FOODON"
        json_str = json.dumps(data, indent=4)
    with open("out.json", 'w') as f:
        f.write(json_str)

readJson("environmental-medium-terms-final.json")

