#!/bin/bash

# Check if the -o flag is provided
if [ "$1" == "-o" ]; then
  # Check if the file path is provided after the -o flag
  if [ -z "$2" ]; then
    echo "Error: No file path provided after the -o flag."
    exit 1
  fi
  
  # Get the file path from the second argument
  FILE_PATH=$2
  
  # Write "Hello" to the file, creating it if it doesn't exist
  echo "Hello" > "$FILE_PATH"
else
  # If no -o flag, print "Hello" to the console
  echo "Hello"
fi
