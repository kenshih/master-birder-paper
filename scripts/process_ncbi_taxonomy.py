#!/usr/bin/env python3
"""
Process the large NCBI Taxonomy OWL file using Jena-based approach.
"""

import sys
from pathlib import Path
import time

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from jena_owl_processor import JenaOWLProcessor

def main():
    """Process the large NCBI taxonomy file."""
    
    # Initialize processor
    processor = JenaOWLProcessor()
    
    # Get file paths
    project_root = Path(__file__).parent.parent
    ncbi_file = project_root / "data" / "ontology" / "ncbitaxon.owl"
    db_file = project_root / "data" / "ncbitaxon.db"
    
    if not ncbi_file.exists():
        print(f"NCBI file not found: {ncbi_file}")
        return
    
    # Show file info
    size_gb = ncbi_file.stat().st_size / (1024 * 1024 * 1024)
    print(f"Processing NCBI Taxonomy OWL file...")
    print(f"File: {ncbi_file.name}")
    print(f"Size: {size_gb:.1f} GB")
    print(f"Output database: {db_file}")
    
    # Confirm processing
    response = input(f"\nThis will process a {size_gb:.1f}GB file. Continue? (y/N): ")
    if response.lower() != 'y':
        print("Processing cancelled.")
        return
    
    # Process to database
    print("\nStarting database processing...")
    print("This may take several minutes...")
    
    start_time = time.time()
    stats = processor.process_to_database(ncbi_file, db_file)
    processing_time = time.time() - start_time
    
    print(f"\nProcessing completed in {processing_time:.1f} seconds")
    print("\nResults:")
    for key, value in stats.items():
        if isinstance(value, int):
            print(f"  {key}: {value:,}")
        else:
            print(f"  {key}: {value}")
    
    # Show some sample queries
    print("\nSample queries you can run:")
    print("1. Find taxonomic ranks:")
    print("   SELECT object, COUNT(*) as count FROM triples WHERE predicate = 'http://purl.obolibrary.org/obo/NCBITaxon_rank' GROUP BY object ORDER BY count DESC LIMIT 10")
    
    print("\n2. Find bird-related taxa:")
    print("   SELECT subject, object FROM triples WHERE (subject LIKE '%bird%' OR object LIKE '%bird%' OR subject LIKE '%Aves%' OR object LIKE '%Aves%') AND predicate = 'http://www.w3.org/2000/01/rdf-schema#label' LIMIT 10")
    
    print("\n3. Find species with common names:")
    print("   SELECT subject, object FROM triples WHERE predicate = 'http://purl.obolibrary.org/obo/NCBITaxon_common_name' LIMIT 10")

if __name__ == "__main__":
    main()
