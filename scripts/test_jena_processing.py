#!/usr/bin/env python3
"""
Test script to demonstrate Jena-based OWL processing.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from jena_owl_processor import JenaOWLProcessor

def main():
    """Test the Jena OWL processor with the available files."""
    
    # Initialize processor
    processor = JenaOWLProcessor()
    
    # Get file paths
    project_root = Path(__file__).parent.parent
    ontology_dir = project_root / "data" / "ontology"
    
    # Test with TaxMeOn (smaller file)
    taxmeon_file = ontology_dir / "taxmeon.owl"
    output_dir = project_root / "data" / "processed" / "taxmeon"
    
    if taxmeon_file.exists():
        print(f"Testing with {taxmeon_file.name}...")
        print(f"File size: {taxmeon_file.stat().st_size / 1024:.1f} KB")
        
        # Process with streaming method
        stats = processor.process_with_rdflib_streaming(taxmeon_file, output_dir)
        
        print("\nProcessing Results:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
        # Test database method
        db_file = project_root / "data" / "taxmeon_test.db"
        print(f"\nTesting database storage...")
        db_stats = processor.process_to_database(taxmeon_file, db_file)
        
        print("Database Results:")
        for key, value in db_stats.items():
            print(f"  {key}: {value}")
            
        # Test a simple query
        query = "SELECT COUNT(*) as total_triples FROM triples"
        df = processor.query_database(db_file, query)
        print(f"\nQuery result: {df.iloc[0]['total_triples']} triples in database")
        
    else:
        print(f"TaxMeOn file not found: {taxmeon_file}")
    
    # Show NCBI file info
    ncbi_file = ontology_dir / "ncbitaxon.owl"
    if ncbi_file.exists():
        size_gb = ncbi_file.stat().st_size / (1024 * 1024 * 1024)
        print(f"\nNCBI Taxonomy file available: {size_gb:.1f} GB")
        print("This file is very large - consider using database storage method")
    else:
        print(f"NCBI file not found: {ncbi_file}")

if __name__ == "__main__":
    main()
