
## Constants 
##
## All the constants used within the API
##

from config.config import API_ENDPOINT

QUERIES = [
    {
        "name": "count-nodes",
        "route": f"{API_ENDPOINT}/node/count",
        "method": "GET",
        "filePath": "queries/count-nodes-for-all-graphs.sparql",
        "description": """
            Return the number of nodes for each graphs present in the virtuoso server. 
        """,
        "parameters": {}
    },
    {
        "name": "count-samples-by-people",
        "route": f"{API_ENDPOINT}/sample/count/people",
        "method": "GET",
        "filePath": "queries/count-samples-by-people.sparql",
        "description": """
            Return the count of the samples for every person that uploded some in the abromics kg
        """,
        "parameters": {}
    },
    {
        "name": "count-samples-by-countries",
        "route": f"{API_ENDPOINT}/sample/count/countries",
        "method": "GET",
        "filePath": "queries/count-samples-by-countries.sparql",
        "description": """
            Return the count of the samples by countries that uploded some in the abromics kg
        """,
        "parameters": {}
    },
    {
        "name": "get-organs-for-specie",
        "route": f"{API_ENDPOINT}/organ",
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
        "route": f"{API_ENDPOINT}/res-genes/best",
        "method": "POST",
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
        "route": f"{API_ENDPOINT}/sample-sources",
        "method": "POST",
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
        "route": f"{API_ENDPOINT}/microorganisms",
        "method": "GET",
        "filePath": "queries/microorganisms/get-microorganism-specie-names.sparql",
        "description": """
            Get the names of all the microoganisms (bacterias) present in the ncbitaxon ontology
        """
    },
    {
        "name": "get-host-specie-names",
        "route": f"{API_ENDPOINT}/hosts",
        "method": "GET",
        "filePath": "queries/hosts/get-host-specie-names.sparql",
        "description": """
            Get all the host species present in the ncbitaxon ontology
        """
    },
    {
        "name": "get-popular-sample-sources",
        "route": f"{API_ENDPOINT}/sample-sources/popular",
        "method": "GET",
        "filePath": "queries/sample-sources/get-popular-anatomical-structures-animal-no-specie.sparql",
        "description": """
            Get the most popular sample sources. Used to get an insight on
            the most used sample sources in the graph.
        """
    }
]

ADMIN_QUERIES = [
    {
        "name": "delete-all-nodes",
        "route": f"{API_ENDPOINT}/graph",
        "method": "DELETE",
        "filePath": "queries/delete-all-nodes.sparql",
        "description": """
            Delete all the nodes present in the knowledge graph 
        """
    }
]
