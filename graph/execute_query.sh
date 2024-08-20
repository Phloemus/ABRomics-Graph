#!/bin/bash

# Check if the file path is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <file-containing-sparql-query>"
  exit 1
fi

# Read the SPARQL query from the file
SPARQL_QUERY=$(<"$1")

# Send the query to the Virtuoso SPARQL endpoint
RESPONSE=$(curl -s --data-urlencode "query=$SPARQL_QUERY" \
              -H "Accept: text/tab-separated-values" \
              "http://localhost:8081/sparql")

# Check if the response is not empty
if [ -z "$RESPONSE" ]; then
  echo "No response received from the SPARQL endpoint."
  exit 1
fi

# Format the result to be readable in the terminal
echo -e "\n--- Query Result ---\n"
echo "$RESPONSE" | column -t -s $'\t'
echo -e "\n--- End of Result ---\n"
