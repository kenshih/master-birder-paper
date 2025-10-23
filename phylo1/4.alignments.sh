#!/bin/bash

# BUSCO Gene Processing and Phylogenetic Analysis Pipeline
# Run this after BUSCO analysis is complete

# eval "$(mamba shell hook --shell zsh)"
# mamba activate phylo
unset PYTHONPATH

# echo "=== Step 1: Extract single-copy BUSCO genes present in all species ==="
# # python extract_busco_genes.py

echo "=== Step 2: Align individual genes with MAFFT ==="
mkdir -p alignments
cd orthologous_genes

gene_count=0
for gene_file in *.fna; do
    if [ -f "$gene_file" ]; then
        gene_name=$(basename "$gene_file" .fna)
        echo "Aligning gene $gene_name..."
        mafft --auto "$gene_file" > "../alignments/${gene_name}_aligned.fna"
        gene_count=$((gene_count + 1))
        
        # Progress indicator
        if [ $((gene_count % 50)) -eq 0 ]; then
            echo "Aligned $gene_count genes..."
        fi
    fi
done

cd ../alignments
echo "Aligned $gene_count genes total"