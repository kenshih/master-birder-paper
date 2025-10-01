#!/bin/bash
# ROBOT script with increased memory for large OWL files

# Set Java heap size to 8GB (adjust based on your system)
export JAVA_OPTS="-Xmx8g -Xms2g"

# Run ROBOT with increased memory
./robot extract \
  --method MIREOT \
  --input data/ontology/ncbitaxon.owl \
  --lower-terms obo:NCBITaxon_8825 \
  --intermediates all --copy-ontology-annotations true \
  --output data/ontology/ncbitaxon_neornithes_raw.owl
