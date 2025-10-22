"""
Extract BUSCO domain sequences from compleasm results
Uses hmmer_output coordinates to extract domains from gene_marker.fasta
"""
import os
import sys
from pathlib import Path
import re

def load_fasta_sequences(fasta_file):
    """Load all sequences from a FASTA file into a dictionary"""
    sequences = {}
    current_id = None
    current_seq = []

    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                # Save previous sequence
                if current_id and current_seq:
                    sequences[current_id] = ''.join(current_seq)

                # Start new sequence
                current_id = line[1:]  # Remove '>'
                current_seq = []
            else:
                current_seq.append(line)

    return sequences

def parse_hmmer_output(hmmer_file, busco_id):
    """Parse hmmer output to get best domain coordinates"""
    if not hmmer_file.exists():
        return None

    best_hit = None
    best_score = -float('inf')

    with open(hmmer_file, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) >= 17:
                target_name = parts[0]
                query_name = parts[3]
                score = float(parts[7])
                from_pos = int(parts[15])  # Start position in protein (1-based)
                to_pos = int(parts[16])    # End position in protein (1-based)
                # Keep best scoring hit

    parts = line.strip().split()
    if len(parts) >= 17:
        target_name = parts[0]
        query_name = parts[3]
        score = float(parts[7])
        from_pos = int(parts[15])  # Start position in protein (1-based)
        to_pos = int(parts[16])    # End position in protein (1-based)

    # Keep best scoring hit
    if score > best_score:
    best_score = score
    best_hit = {
    'target_name': target_name,
    'from_pos': from_pos,
    'to_pos': to_pos,
    'score': score
    }

    return best_hit

def parse_compleasm_table(compleasm_dir, species_name):
    """Parse compleasm full_table to get complete single-copy genes"""
    table_file = Path(compleasm_dir) / "sauropsida_odb12" / "full_table_busco_format.tsv"

    if not table_file.exists():
        print(f"ERROR: Could not find {table_file}")
        return set()

    single_copy_genes = set()
    with open(table_file, 'r') as f:
        for line in f:
            if line.startswith('#'):
               continue
    parts = line.strip().split('\t')
    if len(parts) >= 2:
        busco_id = parts[0]
        status = parts[1]
        if status == "Complete":
            single_copy_genes.add(busco_id)

            print(f"{species_name}: Found {len(single_copy_genes)} single-copy BUSCO genes")
            return single_copy_genes
    if status == "Complete":
    single_copy_genes.add(busco_id)

    print(f"{species_name}: Found {len(single_copy_genes)} single-copy BUSCO genes")
    return single_copy_genes

def extract_busco_domain_sequence(sequences_dict, hmmer_dir, busco_id, species_name):
    """Extract BUSCO domain from full protein using hmmer coordinates"""

    # Parse hmmer output for this BUSCO gene
    hmmer_file = hmmer_dir / f"{busco_id}.out"
    hit_info = parse_hmmer_output(hmmer_file, busco_id)

    if not hit_info:
    return None

    # Find the corresponding protein sequence
    target_name = hit_info['target_name']
    if target_name not in sequences_dict:
    # Sometimes the target name might be slightly different, try to find a match
    for seq_id in sequences_dict.keys():
    if seq_id.startswith(f"{busco_id}_"):
    target_name = seq_id
    break
    else:
    print(f"Warning: Could not find sequence for {target_name}")
    return None

    # Extract domain region (convert to 0-based indexing)
    full_sequence = sequences_dict[target_name]
    from_pos = hit_info['from_pos'] - 1  # Convert to 0-based
    to_pos = hit_info['to_pos']          # End position (exclusive in Python)

    domain_sequence = full_sequence[from_pos:to_pos]

    return f">{species_name}\n{domain_sequence}"

def main():
    species_list = ["chicken", "hummingbird", "duck", "lizard"]
    compleasm_dirs = {sp: f"compleasm/{sp}_compleasm/" for sp in species_list}

    # Parse compleasm results for each species
    species_genes = {}
    species_sequences = {}

    for species, compleasm_dir in compleasm_dirs.items():
    if not os.path.exists(compleasm_dir):
    print(f"ERROR: {compleasm_dir} not found. Run compleasm first!")
    sys.exit(1)

    # Parse BUSCO table
    species_genes[species] = parse_compleasm_table(compleasm_dir, species)

    # Load all sequences once per species
    fasta_file = Path(compleasm_dir) / "sauropsida_odb12" / "gene_marker.fasta"
    if fasta_file.exists():
    print(f"Loading sequences for {species}...")
    species_sequences[species] = load_fasta_sequences(fasta_file)
    else:
    print(f"ERROR: {fasta_file} not found!")
    sys.exit(1)

    # Find genes present in ALL species
    common_genes = None
    for species, genes in species_genes.items():
    if common_genes is None:
    common_genes = genes.copy()
    else:
    common_genes &= genes

    print(f"\nGenes present in ALL species: {len(common_genes)}")

    if len(common_genes) < 50:
    print("WARNING: Very few common genes found. Check compleasm results.")
    return

    # Create output directory
    output_dir = Path("orthologous_domains")
    output_dir.mkdir(exist_ok=True)

    # Extract domain sequences for common genes
    extracted_count = 0
    for busco_id in sorted(common_genes):
    gene_file = output_dir / f"{busco_id}.faa"
    sequences = []

    for species in species_list:
    compleasm_dir = Path(compleasm_dirs[species])
    hmmer_dir = compleasm_dir / "sauropsida_odb12" / "hmmer_output"

    seq = extract_busco_domain_sequence(
    species_sequences[species],
    hmmer_dir,
    busco_id,
    species
    )
    if seq:
    sequences.append(seq)

    if len(sequences) == len(species_list):
    with open(gene_file, 'w') as f:
    f.write('\n'.join(sequences))
    extracted_count += 1

    if extracted_count % 100 == 0:
    print(f"Extracted {extracted_count} domain sequences...")

    print(f"\nSuccessfully extracted {extracted_count} orthologous domain sequences!")
    print(f"Domain files saved in: {output_dir}")

    # Show example of extracted sequence length
    if extracted_count > 0:
    example_file = next(output_dir.glob("*.faa"))
    with open(example_file, 'r') as f:
    content = f.read()
    # Count sequence length (excluding headers)
    seq_lines = [line for line in content.split('\n') if line and not line.startswith('>')]
    if seq_lines:
    example_length = len(''.join(seq_lines)) // len(species_list)
    print(f"Example domain length: ~{example_length} amino acids (vs {4000}+ in full proteins)")

if __name__ == "__main__":
    main()