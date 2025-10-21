"""
Extract single-copy BUSCO genes that are present in all species

writes these protein sequences to ./orthologous_genes/

"""
import os
import sys
from pathlib import Path

def parse_compleasm_table(compleasm_dir, species_name):
    """Parse compleasm-BUSCO full_table to get complete single-copy genes"""
    table_file = None
    for file in Path(compleasm_dir).glob("sauropsida_odb12/full_table_busco_format.tsv"):
        table_file = file
        break
    
    if not table_file:
        print(f"ERROR: Could not find full_table for {species_name}")
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

def extract_sequences(compleasm_dir, busco_id, species_name):
    """Extract protein sequence for a BUSCO gene from compleasm output"""
    # Compleasm stores all sequences in translated_protein.fasta
    protein_file = Path(compleasm_dir) / "sauropsida_odb12" / "translated_protein.fasta"
    
    if not protein_file.exists():
        print(f"ERROR: {protein_file} not found for {species_name}")
        return None
    
    # Read the protein file and extract the specific BUSCO gene sequence
    with open(protein_file, 'r') as f:
        content = f.read()
    
    # Look for the BUSCO gene sequence
    # The header format in compleasm is: >{busco_id}_{some_id}
    lines = content.split('\n')
    current_sequence = []
    in_target_sequence = False
    
    for line in lines:
        if line.startswith('>'):
            # Check if this is our target BUSCO gene
            if line.startswith(f">{busco_id}_"):
                in_target_sequence = True
                current_sequence = [f">{species_name}"]  # Replace header with species name
            else:
                in_target_sequence = False
        elif in_target_sequence and line.strip():
            current_sequence.append(line)
    
    if current_sequence:
        return '\n'.join(current_sequence)
    
    return None

def main():
    species_list = ["chicken", "hummingbird", "duck", "lizard"]
    compleasm_dirs = {sp: f"compleasm/{sp}_compleasm/" for sp in species_list}
    
    # Parse compleasm results for each species
    species_genes = {}
    for species, compleasm_dir in compleasm_dirs.items():
        if not os.path.exists(compleasm_dir):
            print(f"ERROR: {compleasm_dir} not found. Run compleasm first!")
            sys.exit(1)
        species_genes[species] = parse_compleasm_table(compleasm_dir, species)
    
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
    output_dir = Path("orthologous_genes")
    output_dir.mkdir(exist_ok=True)
    
    # Extract sequences for common genes
    extracted_count = 0
    for busco_id in sorted(common_genes):
        gene_file = output_dir / f"{busco_id}.faa"  # Changed to .faa for protein sequences
        sequences = []
        
        for species in species_list:
            compleasm_dir = compleasm_dirs[species]
            seq = extract_sequences(compleasm_dir, busco_id, species)
            if seq:
                sequences.append(seq)
        
        if len(sequences) == len(species_list):
            with open(gene_file, 'w') as f:
                f.write('\n'.join(sequences))
            extracted_count += 1
        
        # print(f"[debug] len(sequences): {len(sequences)}, len(species_list): {len(species_list)}")

        if extracted_count % 100 == 0:
            print(f"Extracted {extracted_count} genes...")
    
    print(f"\nSuccessfully extracted {extracted_count} orthologous genes!")
    print(f"Gene files saved in: {output_dir}")

if __name__ == "__main__":
    main()