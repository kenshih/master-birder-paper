#cd ../trimmed_alignments
print("=== Step 4: Concatenate alignments into supermatrix ===")

# Create concatenated alignment
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
alignment_files = list(Path('./alignments/trimmed_alignments/').glob('*_trimmed.fna'))

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
write_fasta(concatenated_seqs, './concatenated_alignment.fna')

print(f"Concatenated alignment created!")
print(f"Species: {len(species_names)}")
print(f"Total alignment length: {len(list(concatenated_seqs.values())[0])} bp")
print(f"Genes included: {len(alignment_files)}")