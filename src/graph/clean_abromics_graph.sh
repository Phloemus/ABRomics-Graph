#!/bin/bash

# Define the connection parameters
ISQL_PATH="/usr/local/virtuoso-opensource/bin/isql-v" # Adjust the path if necessary
HOST="localhost"
PORT="1111"
USER="dba"
PASSWORD="dba"

# Define the graph to be cleared
GRAPH_URI="http://data.abromics.fr"

# Execute the commands
$ISQL_PATH $HOST:$PORT $USER $PASSWORD <<EOF
SPARQL CLEAR GRAPH <$GRAPH_URI>;
quit;
EOF

# Output result
echo "Graph <$GRAPH_URI> has been cleared on Virtuoso server at $HOST:$PORT."
