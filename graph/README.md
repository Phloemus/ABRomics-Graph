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
