#!/bin/bash
# Extract Neornithes using ROBOT with increased memory

# Set Java heap size to 8GB
export JAVA_OPTS="-Xmx8g -Xms2g"

# Extract Neornithes (NCBITaxon_8825) and all descendants down to species level
./robot extract \
  --method MIREOT \
  --input data/ontology/ncbitaxon.owl \
  --lower-terms obo:NCBITaxon_8825 \
  --intermediates all \
  --copy-ontology-annotations true \
  --output data/ontology/neornithes_robot.owl

echo "Extraction complete: data/ontology/neornithes_robot.owl"
