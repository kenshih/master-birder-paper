"""
Extract single-copy BUSCO genes that are present in all species

writes these genes to ./orthologous_genes/

"""
import os
import sys
from pathlib import Path

def parse_busco_table(busco_dir, species_name):
    """Parse BUSCO full_table to get complete single-copy genes"""
    table_file = None
    for file in Path(busco_dir).glob("run_*/full_table*.tsv"):
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

def extract_sequences(busco_dir, busco_id, species_name):
    """Extract DNA sequence for a BUSCO gene"""
    # Look for sequence files
    seq_dir = Path(busco_dir) / "run_aves_odb12" / "busco_sequences" / "single_copy_busco_sequences"
    
    # print(f"seq_dir: {seq_dir}")
    for seq_file in seq_dir.glob(f"{busco_id}.faa"):
        with open(seq_file, 'r') as f:
            content = f.read()
            # Replace header with species name
            lines = content.split('\n')
            if lines[0].startswith('>'):
                lines[0] = f">{species_name}"
            return '\n'.join(lines)
    
    return None

def main():
    species_list = ["chicken", "hummingbird", "duck"] #, "alligator"]
    busco_dirs = {sp: f"{sp}_busco" for sp in species_list}
    
    # Parse BUSCO results for each species
    species_genes = {}
    for species, busco_dir in busco_dirs.items():
        if not os.path.exists(busco_dir):
            print(f"ERROR: {busco_dir} not found. Run BUSCO first!")
            sys.exit(1)
        species_genes[species] = parse_busco_table(busco_dir, species)
    
    # Find genes present in ALL species
    common_genes = None
    for species, genes in species_genes.items():
        if common_genes is None:
            common_genes = genes.copy()
        else:
            common_genes &= genes
    
    print(f"\nGenes present in ALL species: {len(common_genes)}")
    
    if len(common_genes) < 50:
        print("WARNING: Very few common genes found. Check BUSCO results.")
        return
    
    # Create output directory
    output_dir = Path("orthologous_genes")
    output_dir.mkdir(exist_ok=True)
    
    # Extract sequences for common genes
    extracted_count = 0
    for busco_id in sorted(common_genes):
        gene_file = output_dir / f"{busco_id}.fna"
        sequences = []
        
        for species in species_list:
            busco_dir = busco_dirs[species]
            seq = extract_sequences(busco_dir, busco_id, species)
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