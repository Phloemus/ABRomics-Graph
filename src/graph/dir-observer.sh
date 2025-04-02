#!/bin/bash

## Allows to load the the ttl files when added or modified in the "ontologies" or "graph-instance" 
## directories automatically

# Directories to monitor
LOG_FILE="/changes.log"

# Check if the directory exists
if [ ! -d "$DATA_DIR" ]; then
  echo "Directory $DATA_DIR does not exist. Exiting." > "$LOG_FILE"
  exit 1
fi

# Check if the directory exists
if [ ! -d "$ONTOLOGY_DIR" ]; then
  echo "Directory $ONTOLOGY_DIR does not exist. Exiting." > "$LOG_FILE"
  exit 1
fi

# Use inotifywait to listen for creation or modify events in the directory
inotifywait -m -r -e create -e modify --format '%w%f %e %T' --timefmt '%Y-%m-%d %H:%M:%S' "$DATA_DIR" |
while read FILE EVENT TIMESTAMP
do
  # Log the event to the log file
  if [[ "$EVENT" == "CREATE" || "$EVENT" == "MODIFY" ]]; then
    filename=$(basename "$FILE")
    echo "ld_dir_all('$DATA_DIR', '$filename', '$DEFAULT_GRAPH');" | isql-v -U dba -P dba
    isql-v -U dba -P dba exec="rdf_loader_run();" &
    echo "$TIMESTAMP - File '$FILE' was $EVENT" >> "$LOG_FILE"
  fi
done
