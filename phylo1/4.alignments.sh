#!/bin/bash

# BUSCO Gene Processing and Phylogenetic Analysis Pipeline
# Run this after BUSCO analysis is complete

eval "$(mamba shell hook --shell zsh)"
mamba activate phylo
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

echo "=== Step 3: Trim alignments with TrimAl ==="
mkdir -p trimmed_alignments

for alignment in *_aligned.fna; do
    if [ -f "$alignment" ]; then
        gene_name=$(basename "$alignment" _aligned.fna)
        echo "Trimming $gene_name..."
        trimal -in "$alignment" -out "../trimmed_alignments/${gene_name}_trimmed.fna" -automated1
    fi
done

cd ../trimmed_alignments
echo "=== Step 4: Concatenate alignments into supermatrix ==="

# Create concatenated alignment
python << 'EOF'
import os
from pathlib import Path

def read_fasta(filename):
    """Read a FASTA file and return sequences as dict"""
    sequences = {}
    current_seq = None
    current_name = None
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_name and current_seq:
                    sequences[current_name] = current_seq
                current_name = line[1:]  # Remove >
                current_seq = ""
            else:
                current_seq += line
    
    if current_name and current_seq:
        sequences[current_name] = current_seq
    
    return sequences

def write_fasta(sequences, filename):
    """Write sequences to FASTA file"""
    with open(filename, 'w') as f:
        for name, seq in sequences.items():
            f.write(f">{name}\n{seq}\n")

# Get all species names from first alignment file
species_names = None
alignment_files = list(Path('.').glob('*_trimmed.fna'))

if not alignment_files:
    print("ERROR: No trimmed alignment files found!")
    exit(1)

# Initialize concatenated sequences
concatenated_seqs = {}

# Process each alignment file
for i, align_file in enumerate(sorted(alignment_files)):
    print(f"Processing {align_file.name} ({i+1}/{len(alignment_files)})...")
    
    seqs = read_fasta(align_file)
    
    # Initialize species on first file
    if species_names is None:
        species_names = set(seqs.keys())
        for species in species_names:
            concatenated_seqs[species] = ""
    
    # Check all species are present
    if set(seqs.keys()) != species_names:
        print(f"WARNING: Species mismatch in {align_file.name}")
        continue
    
    # Add sequences to concatenated alignment
    for species in species_names:
        concatenated_seqs[species] += seqs[species]

# Write concatenated alignment
write_fasta(concatenated_seqs, '../concatenated_alignment.fna')

print(f"Concatenated alignment created!")
print(f"Species: {len(species_names)}")
print(f"Total alignment length: {len(list(concatenated_seqs.values())[0])} bp")
print(f"Genes included: {len(alignment_files)}")
EOF

cd ..

echo "=== Step 5: Build phylogenetic tree with IQ-TREE ==="
echo "Running IQ-TREE with model selection and bootstrap support..."

iqtree -s concatenated_alignment.fna -m MFP -bb 1000 -nt AUTO --prefix bird_phylogeny

echo "=== ANALYSIS COMPLETE! ==="
echo "Results:"
echo "- Phylogenetic tree: bird_phylogeny.treefile"
echo "- Bootstrap tree: bird_phylogeny.contree"
echo "- Log file: bird_phylogeny.log"

echo "View your tree with:"
echo "1. FigTree (GUI): Open bird_phylogeny.contree"
echo "2. Online: Upload to iTOL (https://itol.embl.de/)"

ls -lh bird_phylogeny.*