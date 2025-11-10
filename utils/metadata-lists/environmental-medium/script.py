import json

def readJson(filename):
    ontologies = {}
    with open(filename, 'r') as file:
        data = json.load(file)
        count = 1
        for item in data:
            item["pk"] = count
            if "FOODON" in item["fields"]["class"]:
                item["fields"]["ontology"] = "FOODON"
            count = count + 1
        json_str = json.dumps(data, indent=4)
    with open("out.json", 'w') as f:
        f.write(json_str)

readJson("unformated-list.json")

