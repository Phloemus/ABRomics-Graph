import requests
import xmltodict
import xml.etree.ElementTree as ET
import json
import pandas as pd
import time

df = pd.read_csv("uc3-reports/resfinder-galaxy-results.tsv", sep="\t")
df["SRR"] = df["Contig"].str.split("_").str[0]
print(df["SRR"])

def parse_lat_lon(coord_str):
    lat_str, lat_dir, lon_str, lon_dir = coord_str.split()
    lat, lon = float(lat_str), float(lon_str)
    if lat_dir.upper() == "S": lat = -lat
    if lon_dir.upper() == "W": lon = -lon
    return lat, lon

def getAllSRAIdsFromSRR(srr):
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


unique_srr = df["SRR"].dropna().unique().tolist()

print(f"{len(unique_srr)} unique SRR found")

srr_results = {}
for srr in unique_srr:
    print(f"Fetching {srr}")
    metadata = getAllSRAIdsFromSRR(srr)
    srr_results[srr] = metadata
    time.sleep(0.4)   # Respect NCBI rate limit (3 req/sec)

ncbiIdsDf = pd.DataFrame.from_dict(srr_results, orient="index")

df = df.merge(ncbiIdsDf, on="SRR", how="left")
df.to_csv("file_with_metadata.tsv", sep="\t", index=False)

## Get the sample metadata in the df
unique_samn = df["SAMN"].dropna().unique().tolist()

print(f"{len(unique_srr)} unique SAMN found")
print("Getting the biosample metadata from NCBI")

samn_results = {}
for samn in unique_samn:
    print(f"Fetching {samn}")
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
            latitude, longitude = parse_lat_lon(attribute['#text'])
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

samnMetadataDf = pd.DataFrame.from_dict(samn_results, orient="index")

df = df.merge(samnMetadataDf, on="SAMN", how="left")

## Generate the sample metadata section of the report
print("Generating the analysis reports")
reportsCounter = 0
samplesDf = df.drop_duplicates(subset=["SAMN"], keep="first")
print(samplesDf["SAMN"])
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

    with open(f"uc3-reports/report_{sample['SAMN']}.json", "w", encoding="utf-8") as f:
        json.dump(reportDict, f, indent=2)
    print(f"report for sample {sample['SAMN']} created in ./uc3-reports")
    reportsCounter += 1
print(f"{reportsCounter} reports generated")