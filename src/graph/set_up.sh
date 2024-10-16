
# Tracks the data of these files
echo "ld_dir_all('/usr/local/virtuoso-opensource/share/virtuoso/vad/graph-instance', '*.ttl', 'http://data.abromics.fr');" | isql-v -U dba -P dba 
echo "ld_dir_all('/usr/local/virtuoso-opensource/share/virtuoso/vad/ontologies', '*.owl', 'http://ontologies.abromics.fr');" | isql-v -U dba -P dba 

# Allows to load the graph data (fetch data from the graph files tracked before)
isql-v -U dba -P dba exec="rdf_loader_run();" &
