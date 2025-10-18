#!/bin/bash

# Activate the phylo environment and set Python path
mamba activate phylo
unset PYTHONPATH

# Create directories
mkdir -p genomes
cd genomes

echo "Downloading bird genomes for phylogenetic analysis..."

# 1. Chicken (Gallus gallus) - RefSeq
echo "Downloading chicken genome..."
datasets download genome accession GCF_000002315.5 --filename chicken_genome.zip
unzip -o chicken_genome.zip -d chicken_genome/
echo "Chicken genome downloaded successfully"

# 2. Anna's Hummingbird (Calypte anna)
echo "Downloading Anna's hummingbird genome..."
datasets download genome accession GCA_003957565.1 --filename hummingbird_genome.zip
unzip -o hummingbird_genome.zip -d hummingbird_genome/
echo "Hummingbird genome downloaded successfully"

# 3. Mallard Duck (Anas platyrhynchos)
echo "Downloading mallard duck genome..."
datasets download genome accession GCA_002592135.1 --filename duck_genome.zip  
unzip -o duck_genome.zip -d duck_genome/
echo "Duck genome downloaded successfully"

# # 4. American Alligator (Alligator mississippiensis) - Outgroup
# echo "Downloading American alligator genome (outgroup)..."
# datasets download genome accession GCA_000281125.1 --filename alligator_genome.zip
# unzip -o alligator_genome.zip -d alligator_genome/
# echo "Alligator genome downloaded successfully"
datasets download genome accession GCF_000344595.1 --filename turtle_genome.zip
unzip -o turtle_genome.zip -d turtle_genome/


# Turtle

echo "All genomes downloaded!"
echo "Next step: Run BUSCO analysis on each genome"

# List the downloaded files
echo "Downloaded genome files:"
find . -name "*.fna" | head -10