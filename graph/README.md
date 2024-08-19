# Graph directory

The graph directory is a place where all the files that containing the data of the graph are stored. 
As such, there is two different types of files stored here:

1. **ontologies :** *(in the ***ontology*** *directory)* It contains the specific ontologies used 
   in the graph. Usually the ontologies stored there are large dictionnaries of terms in the **owl**
   or **xml** formats. There are no instanciation of data, the files of the directory only contains
   the vocabulary used in the knowledge graph.
2. **graph-instance :** *(in the ***graph-instance*** *directory)* It contains the real graph database
   of the ABRomics project where there is the concrete data. The classes defined in the vocabulary 
   provided in the by the ontologies are instanciated into realy data.

The graph files contained in the **graph-instance** directory may be very large. As such they might 
be stored somewhere else in the future. This will require to use a tool to download the large files from a 
specific server able to store large amount of data. 

When launching the project on a new machine the **graph-instance** doesn't contain the files containing the 
abromics data. A launching script have to be launch to fetch data from the ABRomics database and replicate
them over in a graph format with ontologies annotations.

Later the REST API of ABRomics KG can be used to add data in the graph or retrive data from the graph. The
REST API may be used in several parts of the ABRomics whole codebase. It's a tool allowing the dev to no 
having to perform SPARQL requests directly even though using SPARQL requests via the sparql endpoint of the 
ABRomics project server is the way to go for custom queries

To load the graphs files into the virtuoso graph server. Complete the set up of the docker containers by 
telling virtuoso to consume the files present in **ontologies** and **graph-instance**

```
bash 
# after doing a docker compose up -d
# check the container launched and copy the container id
docker ps | grep virtuoso 
```

```
bash
# get the ID of the container called abromics-virtuoso and execute the following command
docker exec -it <containerID> sh
```

Normally you should be in the shell of the abromics-virtuoso container

```
bash 
# execute the script that intergrated the data of the graph files into the virtuoso graph database
cd /usr/local/virtuoso-opensource/share/virtuoso/vad
chmod +x set_up.sh
./set_up.sh
# The command can take time but wait until the script finish (it should show "Done. -- xxxxx msec.")
```

Now all the nodes present in the included graph files should be displonible in the graph when performing
a SPARQL query. To check this go to **localhost:8081/sparql** and perform the following query in to count
the number of the different graph. The graph that holds the abromics data is called http://data.abromics.fr

```
SELECT ?graph (COUNT(?s) AS ?tripleCount)
WHERE {
  GRAPH ?graph {
    ?s ?p ?o .
  }
}
GROUP BY ?graph
ORDER BY DESC(?tripleCount)
```

## Deleting all the abromics data

It's possible to clear the data of the abromics graph by running the **clear_abromics_graph.sh**

```
bash
cd /usr/local/virtuoso-opensource/share/virtuoso/vad
chmod +x clear_abromics_graph.sh
./clear_abromics_graph.sh
```

## Loading new data

Adding new data can be done using SPARQL requests (for small data addition). However, this process is not
very efficient for large data update. In the case of a large update or addition of data. It's more relevant 
to generate new ttl files that can be added in the **graph-instance** directory.

When adding ttl files in **graph-instance** directory, virtuoso will not automatically update the graph database.
To update it use execute the **clear_abromics_graph.sh** (in /usr/local/virtuoso-opensource/share/virtuoso/vad) script 
in the virutoso container and then load it back using the **load.sh** script. 
The script will make virutoso reload all the ttl files.

