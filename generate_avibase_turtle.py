#!/usr/bin/env python3
"""
Generate Turtle file with AvibaseID instances from database query
"""

import sqlite3
import sys

def generate_avibase_turtle(db_path, output_file):
    """Generate Turtle file with AvibaseID instances"""
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute the query
    query = """
    SELECT a.avibase_id, n.ncbi_taxon_id, n.scientific_name
    FROM AvibaseID a
    JOIN NCBITaxonID n ON a.concept_label = n.scientific_name
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Generate Turtle content
    turtle_content = []
    
    # Add prefixes
    turtle_content.extend([
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
        "@prefix obo: <http://purl.obolibrary.org/obo/> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "@prefix mb: <http://kenshih.com/master-birder/ontology#> .",
        ""
    ])
    
    # Process each row
    for avibase_id, ncbi_taxon_id, scientific_name in rows:
        # Clean up the NCBI taxon ID (remove full URI if present)
        if ncbi_taxon_id.startswith('http://purl.obolibrary.org/obo/NCBITaxon_'):
            ncbi_id = ncbi_taxon_id.split('NCBITaxon_')[-1]
        else:
            ncbi_id = ncbi_taxon_id
            
        # Create URIs
        avibase_instance = f"mb:AvibaseID_{avibase_id}"
        ncbi_taxon = f"obo:NCBITaxon_{ncbi_id}"
        avibase_url = f"https://avibase.bsc-eoc.org/species.jsp?avibaseid={avibase_id}"
        
        # Generate Turtle for the NCBI taxon with hasAvibaseIdentifier
        turtle_content.extend([
            f"{ncbi_taxon}",
            f"  mb:hasAvibaseIdentifier {avibase_instance} .",
            ""
        ])
        
        # Generate Turtle for the AvibaseID instance
        turtle_content.extend([
            f"{avibase_instance}",
            f"  rdf:type mb:AvibaseIdentifier ;",
            f"  mb:identifierValue \"{avibase_id}\" ;",
            f"  rdfs:seeAlso <{avibase_url}> ;",
            f"  rdfs:label \"{scientific_name}\" .",
            ""
        ])
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(turtle_content))
    
    conn.close()
    print(f"Generated {len(rows)} AvibaseID instances in {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_avibase_turtle.py <database_path> <output_file>")
        sys.exit(1)
    
    db_path = sys.argv[1]
    output_file = sys.argv[2]
    
    generate_avibase_turtle(db_path, output_file)
