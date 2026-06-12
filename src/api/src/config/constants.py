
## Constants 
##
## All the constants used within the API
##

from config.config import API_ENDPOINT, API_BASEPATH

COMPETENCY_QUESTION_QUERIES = [
    {
        "id": 1,
        "adminOnly": False,
        "title": "What are the most common antibiotic resistance genes in all samples ?",
        "name": "competency question 1",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/query/competency-question/1",
        "smallRoute": "query/competency-question/1",
        "description": "This competency question allows to explore the whole database in order to find relevant data for further exploration. The query is a template that can be easily reused to build new SPARQL queries that will rely on different data sources using Uniprot or Wikidata. It serves as the test request when deploying the application, so this query should always work perfectly !",
        "ontologies": [
            {
                "type": "generic",
                "shortName": "SOSA",
                "name": "",
                "description": "Provide a vocabulary to model observations made by a procedure such as a bioinformatics workflow",
                "bioportalUrl": "https://www.w3.org/TR/vocab-ssn/"
            },
            {
                "type": "generic",
                "shortName": "SIO",
                "name": "",
                "description": "The semanticscience integrated ontology (SIO) provides a simple, integrated ontology (types, relations) for objects, processes and..",
                "bioportalUrl": "https://bioportal.bioontology.org/ontologies/SIO"
            },
            {
                "type": "omics",
                "shortName": "NCIT",
                "name": "",
                "description": "reference terminology that includes broad coverage of the cancer domain, including cancer related diseases, findings and..",
                "bioportalUrl": "https://bioportal.bioontology.org/ontologies/NCIT"
            }
        ],
        "queryFilePath": "queries/competency-questions/q1-get-all-res-genes-for-specific-sample.sparql",
        "method": "GET",
        "parameters": {}
    },
    {
        "id": 2,
        "adminOnly": False,
        "title": "What are actively circulating ABR genes, given a specific time-frame",
        "name": "competency question 2",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/query/competency-question/2",
        "smallRoute": "query/competency-question/2",
        "description": "This competency question is a simple example that shows how to only select samples collected in a specific timeframe. ",
        "ontologies": [
            {
                "type": "generic",
                "shortName": "SOSA",
                "name": "",
                "description": "Provide a vocabulary to model observations made by a procedure such as a bioinformatics workflow",
                "bioportalUrl": "https://www.w3.org/TR/vocab-ssn/"
            },
            {
                "type": "generic",
                "shortName": "SIO",
                "name": "",
                "description": "The semanticscience integrated ontology (SIO) provides a simple, integrated ontology (types, relations) for objects, processes and..",
                "bioportalUrl": "https://bioportal.bioontology.org/ontologies/SIO"
            },
            {
                "type": "omics",
                "shortName": "NCIT",
                "name": "",
                "description": "reference terminology that includes broad coverage of the cancer domain, including cancer related diseases, findings and..",
                "bioportalUrl": "https://bioportal.bioontology.org/ontologies/NCIT"
            }
        ],
        "queryFilePath": "queries/competency-questions/q2-circulating-abr-genes-in-timeframe.sparql",
        "method": "GET",
        "parameters": {}
    },
    {
        "id": 3,
        "adminOnly": False,
        "title": "What are the most represented antibiotic resistance genes in a specific geographical region of interest",
        "name": "competency question 3",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/query/competency-question/3",
        "smallRoute": "query/competency-question/3",
        "description": "Filtering genes based on a precise geographical region of interest is key to study the spread of antibiotic resistance genes in the environment. This competency question shows how GPS coordinates can be laverage to select samples collected arround a point and evaluate the resistance genes found",
        "ontologies": [
            {
                "type": "generic",
                "shortName": "SOSA",
                "name": "",
                "description": "Provide a vocabulary to model observations made by a procedure such as a bioinformatics workflow",
                "bioportalUrl": "https://www.w3.org/TR/vocab-ssn/"
            },
            {
                "type": "generic",
                "shortName": "SIO",
                "name": "",
                "description": "The semanticscience integrated ontology (SIO) provides a simple, integrated ontology (types, relations) for objects, processes and..",
                "bioportalUrl": "https://bioportal.bioontology.org/ontologies/SIO"
            },
            {
                "type": "omics",
                "shortName": "NCIT",
                "name": "",
                "description": "reference terminology that includes broad coverage of the cancer domain, including cancer related diseases, findings and..",
                "bioportalUrl": "https://bioportal.bioontology.org/ontologies/NCIT"
            }
        ],
        "queryFilePath": "queries/competency-questions/q3-get-abr-genes-in-geo-location.sparql",
        "method": "GET",
        "parameters": {}
    },
    {
        "id": 4,
        "adminOnly": False,
        "title": "What are the TOP-K antibiotic resistance genes given a certain quality metric",
        "name": "competency question 4",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/query/competency-question/4",
        "smallRoute": "query/competency-question/4",
        "description": "Assessing the quality of a measure perfomed by a workflow is essential to propose relevant scientific conclusions. This competency question shows how the relevancy of the resistance genes discovered by a workflow can be assessed using the identify % metric as an indicator of good gene quality",
        "ontologies": [
            {
                "type": "generic",
                "shortName": "SOSA",
                "name": "",
                "description": "Provide a vocabulary to model observations made by a procedure such as a bioinformatics workflow",
                "bioportalUrl": "https://www.w3.org/TR/vocab-ssn/"
            },
            {
                "type": "generic",
                "shortName": "SIO",
                "name": "",
                "description": "The semanticscience integrated ontology (SIO) provides a simple, integrated ontology (types, relations) for objects, processes and..",
                "bioportalUrl": "https://bioportal.bioontology.org/ontologies/SIO"
            },
            {
                "type": "omics",
                "shortName": "NCIT",
                "name": "",
                "description": "reference terminology that includes broad coverage of the cancer domain, including cancer related diseases, findings and..",
                "bioportalUrl": "https://bioportal.bioontology.org/ontologies/NCIT"
            }
        ],
        "queryFilePath": "queries/competency-questions/q4-genes-filtered-by-identity.sparql",
        "method": "GET",
        "parameters": {}
    },
    {
        "id": 5,
        "adminOnly": False,
        "title": "Between human and animal samples, what are the most shared resistance genes",
        "name": "competency question 5",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/query/competency-question/5",
        "smallRoute": "query/competency-question/5",
        "description": "This competency questions shows how the knowledge graph can help to perform One Health investigations by looking at common antibiotic resistance genes present in the human, animal and environmental reservoirs. Such query can be further completed to perform rich analysis using timeframe filtration and selection of only specific geographical regions of interets",
        "ontologies": [
            {
                "type": "generic",
                "shortName": "SOSA",
                "name": "",
                "description": "Provide a vocabulary to model observations made by a procedure such as a bioinformatics workflow",
                "bioportalUrl": "https://www.w3.org/TR/vocab-ssn/"
            },
            {
                "type": "generic",
                "shortName": "SIO",
                "name": "",
                "description": "The semanticscience integrated ontology (SIO) provides a simple, integrated ontology (types, relations) for objects, processes and..",
                "bioportalUrl": "https://bioportal.bioontology.org/ontologies/SIO"
            },
            {
                "type": "omics",
                "shortName": "NCIT",
                "name": "",
                "description": "reference terminology that includes broad coverage of the cancer domain, including cancer related diseases, findings and..",
                "bioportalUrl": "https://bioportal.bioontology.org/ontologies/NCIT"
            }
        ],
        "queryFilePath": "queries/competency-questions/q5-most-occurent-res-gene-for-geo-region.sparql",
        "method": "GET",
        "parameters": {}
    },
    {
        "id": 6,
        "adminOnly": False,
        "title": "What are all the potentially inefficient antibiotic drugs given a specific sample",
        "name": "competency question 6",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/query/competency-question/6",
        "smallRoute": "query/competency-question/6",
        "description": "This competency questions shows how the ontologies used within the knowledge graph can be used to filter the data even more. For instance, with this query, we use the knowledge given by the ARO ontology to get the list of all the antibiotics that will be ineficient for treating all bacteria strains found in the human samples",
        "ontologies": [
            {
                "type": "generic",
                "shortName": "SOSA",
                "name": "",
                "description": "Provide a vocabulary to model observations made by a procedure such as a bioinformatics workflow",
                "bioportalUrl": "https://www.w3.org/TR/vocab-ssn/"
            },
            {
                "type": "generic",
                "shortName": "SIO",
                "name": "",
                "description": "The semanticscience integrated ontology (SIO) provides a simple, integrated ontology (types, relations) for objects, processes and..",
                "bioportalUrl": "https://bioportal.bioontology.org/ontologies/SIO"
            },
            {
                "type": "omics",
                "shortName": "NCIT",
                "name": "",
                "description": "reference terminology that includes broad coverage of the cancer domain, including cancer related diseases, findings and..",
                "bioportalUrl": "https://bioportal.bioontology.org/ontologies/NCIT"
            }
        ],
        "queryFilePath": "queries/competency-questions/q6-potentialy-inefficient-drugs.sparql",
        "method": "GET",
        "parameters": {}
    }
]

QUERIES = [
    {
        "name": "count-nodes",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/node/count",
        "method": "GET",
        "filePath": "queries/count.sparql",
        "description": """
            Return the number of nodes in the knowledge graph
        """,
        "parameters": {}
    },
    {
        "name": "count-samples-by-people",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/sample/count/people",
        "method": "GET",
        "filePath": "queries/count-samples-by-people.sparql",
        "description": """
            Return the count of the samples for every person that uploded some in the abromics kg
        """,
        "parameters": {}
    },
    {
        "name": "count-samples-by-countries",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/sample/count/countries",
        "method": "GET",
        "filePath": "queries/count-samples-by-countries.sparql",
        "description": """
            Return the count of the samples by countries that uploded some in the abromics kg
        """,
        "parameters": {}
    },
    {
        "name": "get-organs-for-specie",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/organ",
        "method": "POST",
        "filePath": "queries/get-organs-by-specie-name.sparql",
        "description": """
            Get all the organs for a specific specie indicated by a specie_name
        """,
        "parameters": {
            "specie_name": "the name of the selected specie. Should be the latin name of the specie"
        }
    },
    {
        "name": "get-ktop-antibiotic-res-genes",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/res-genes/best",
        "method": "GET",
        "filePath": "queries/q1-search-antibiotic-res-genes-all-sample.sparql",
        "description": """
            Get all the best antibiotic resistance genes for a given metric for all the samples
        """,
        "parameters": {
            "metric": "the label of the feature of interest that the antibiotic resistance genes should be filtered by"
        }
    },
    {
        "name": "get-sample-sources",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/sample-sources",
        "method": "GET",
        "filePath": { 
            "animal": "queries/sample-sources/get-anatomical-structures-animal.sparql",
            "animal-no-specie": "queries/sample-sources/get-anatomical-structures-animal-no-specie.sparql",
            "environmental": "queries/sample-sources/get-sample-sources-environmental.sparql", 
            "all": "queries/sample-sources/get-sample-sources-all.sparql"
        },
        "description": """
            Get all the disponible sample sources
        """,
        "parameters": {
            "specieName": "[optional] The name of the specie the sample source is from",
            "sampleType": "[optional] The type of the sample. Can be human, animal or environmental"
        }
    },
    {
        "name": "get-microorganism-specie-names",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/microorganisms",
        "method": "GET",
        "filePath": "queries/microorganisms/get-microorganism-specie-names.sparql",
        "description": """
            Get the names of all the microoganisms (bacterias) present in the ncbitaxon ontology
        """
    },
    {
        "name": "get-host-specie-names",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/hosts",
        "method": "GET",
        "filePath": "queries/hosts/get-host-specie-names.sparql",
        "description": """
            Get all the host species present in the ncbitaxon ontology
        """
    },
    {
        "name": "get-popular-sample-sources",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/sample-sources/popular",
        "method": "GET",
        "filePath": "queries/sample-sources/get-popular-anatomical-structures-animal-no-specie.sparql",
        "description": """
            Get the most popular sample sources. Used to get an insight on
            the most used sample sources in the graph.
        """
    },
    {
        "name": "get-resistance-gene-aro-class",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/resistance-genes/aro-class",
        "method": "POST",
        "filePath": "queries/resistance-genes/get-resistance-gene-aro-class.sparql",
        "description": """
            From a list of resistance genes labels (name), get the list of the associated aro 
            classes (url) if the resistance gene is found in the ARO ontology
        """,
        "parameters": {
            "resistanceGenes": "The list of the resistance genes labels"
        }
    }
]

ADMIN_QUERIES = [
    {
        "name": "delete-all-nodes",
        "route": f"{API_ENDPOINT}/{API_BASEPATH}/graph",
        "method": "DELETE",
        "filePath": "queries/delete-all-nodes.sparql",
        "description": """
            Delete all the nodes present in the knowledge graph 
        """
    }
]
