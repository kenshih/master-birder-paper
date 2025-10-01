#!/usr/bin/env python3
"""
Extract Neornithes (modern birds) from Fuseki dataset and write to OWL file.
This extracts obo:NCBITaxon_8825 and all descendants down to species level,
excluding subspecies and below.
"""

import requests
import json
from pathlib import Path
import logging
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NeornithesExtractor:
    """Extract Neornithes taxonomy from Fuseki."""
    
    def __init__(self, fuseki_url="http://localhost:3030", dataset_name="ncbitaxon"):
        self.fuseki_url = fuseki_url
        self.dataset_name = dataset_name
        self.sparql_url = f"{fuseki_url}/{dataset_name}/sparql"
        
        # Define namespaces
        self.obo = Namespace("http://purl.obolibrary.org/obo/")
        self.ncbi = Namespace("http://purl.obolibrary.org/obo/NCBITaxon_")
        
    def query_fuseki(self, sparql_query):
        """Execute SPARQL query on Fuseki dataset."""
        try:
            response = requests.get(self.sparql_url, params={'query': sparql_query})
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Query failed: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return None
    
    def get_taxonomic_ranks(self):
        """Get all taxonomic ranks in the dataset."""
        query = """
        PREFIX obo: <http://purl.obolibrary.org/obo/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?rank (COUNT(*) as ?count)
        WHERE {
            ?taxon obo:NCBITaxon_rank ?rank .
        }
        GROUP BY ?rank
        ORDER BY DESC(?count)
        """
        
        result = self.query_fuseki(query)
        if result:
            logger.info("Taxonomic ranks found:")
            for binding in result['results']['bindings']:
                rank = binding['rank']['value']
                count = binding['count']['value']
                logger.info(f"  {rank}: {count}")
            return [binding['rank']['value'] for binding in result['results']['bindings']]
        return []
    
    def get_neornithes_descendants(self):
        """Get all descendants of Neornithes (NCBITaxon_8825) down to species level."""
        
        # First, let's see what ranks we have
        ranks = self.get_taxonomic_ranks()
        
        # Define ranks we want to include (down to species, excluding subspecies)
        included_ranks = [
            "http://purl.obolibrary.org/obo/NCBITaxon_superclass",
            "http://purl.obolibrary.org/obo/NCBITaxon_class", 
            "http://purl.obolibrary.org/obo/NCBITaxon_subclass",
            "http://purl.obolibrary.org/obo/NCBITaxon_superorder",
            "http://purl.obolibrary.org/obo/NCBITaxon_order",
            "http://purl.obolibrary.org/obo/NCBITaxon_suborder",
            "http://purl.obolibrary.org/obo/NCBITaxon_superfamily",
            "http://purl.obolibrary.org/obo/NCBITaxon_family",
            "http://purl.obolibrary.org/obo/NCBITaxon_subfamily",
            "http://purl.obolibrary.org/obo/NCBITaxon_genus",
            "http://purl.obolibrary.org/obo/NCBITaxon_species"
        ]
        
        # Build the rank filter
        rank_filter = " || ".join([f"?rank = <{rank}>" for rank in included_ranks])
        
        query = f"""
        PREFIX obo: <http://purl.obolibrary.org/obo/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT DISTINCT ?taxon ?label ?rank ?parent
        WHERE {{
            # Start from Neornithes
            obo:NCBITaxon_8825 obo:NCBITaxon_has_rank ?neornithes_rank .
            
            # Get all descendants using transitive closure
            ?taxon obo:NCBITaxon_has_rank ?rank .
            ?taxon obo:NCBITaxon_has_rank+ obo:NCBITaxon_8825 .
            
            # Only include ranks down to species (exclude subspecies)
            FILTER ({rank_filter})
            
            # Get labels and parent relationships
            OPTIONAL {{ ?taxon rdfs:label ?label }}
            OPTIONAL {{ ?taxon obo:NCBITaxon_has_rank ?parent }}
        }}
        ORDER BY ?taxon
        """
        
        logger.info("Querying for Neornithes descendants...")
        result = self.query_fuseki(query)
        
        if result:
            logger.info(f"Found {len(result['results']['bindings'])} Neornithes taxa")
            return result['results']['bindings']
        else:
            logger.error("Failed to get Neornithes descendants")
            return []
    
    def get_taxon_triples(self, taxon_uri):
        """Get all triples for a specific taxon."""
        query = f"""
        PREFIX obo: <http://purl.obolibrary.org/obo/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?subject ?predicate ?object
        WHERE {{
            ?subject ?predicate ?object .
            FILTER (?subject = <{taxon_uri}> || ?object = <{taxon_uri}>)
        }}
        """
        
        result = self.query_fuseki(query)
        if result:
            return result['results']['bindings']
        return []
    
    def create_owl_file(self, output_file, taxon_data):
        """Create OWL file with extracted Neornithes data."""
        
        # Create RDF graph
        g = Graph()
        
        # Add namespaces
        g.bind("obo", self.obo)
        g.bind("rdfs", RDFS)
        g.bind("rdf", RDF)
        g.bind("owl", OWL)
        
        # Add ontology header
        ontology_uri = URIRef("http://example.org/neornithes")
        g.add((ontology_uri, RDF.type, OWL.Ontology))
        g.add((ontology_uri, RDFS.label, Literal("Neornithes Taxonomy")))
        g.add((ontology_uri, RDFS.comment, Literal("Extracted Neornithes taxonomy from NCBI")))
        
        # Process each taxon
        processed_taxa = set()
        
        for binding in taxon_data:
            taxon_uri = binding['taxon']['value']
            
            if taxon_uri in processed_taxa:
                continue
                
            processed_taxa.add(taxon_uri)
            
            # Get all triples for this taxon
            triples = self.get_taxon_triples(taxon_uri)
            
            for triple in triples:
                subject = URIRef(triple['subject']['value'])
                predicate = URIRef(triple['predicate']['value'])
                
                # Handle object (could be URI or literal)
                if triple['object']['type'] == 'uri':
                    object_val = URIRef(triple['object']['value'])
                else:
                    object_val = Literal(triple['object']['value'])
                
                g.add((subject, predicate, object_val))
        
        # Serialize to OWL file
        g.serialize(destination=str(output_file), format='xml')
        logger.info(f"Created OWL file: {output_file}")
        logger.info(f"Total triples: {len(g)}")
        logger.info(f"Total taxa: {len(processed_taxa)}")
        
        return len(g), len(processed_taxa)

def main():
    """Extract Neornithes from Fuseki and create OWL file."""
    
    # Initialize extractor
    extractor = NeornithesExtractor()
    
    # Check if Fuseki is accessible
    try:
        response = requests.get(extractor.sparql_url, timeout=5)
        if response.status_code != 200:
            print("Cannot access Fuseki. Make sure it's running at http://localhost:3030")
            return
    except:
        print("Cannot connect to Fuseki server. Please start it first:")
        print("  cd apache-jena-fuseki-5.5.0")
        print("  ./fuseki-server")
        return
    
    # Get Neornithes descendants
    taxon_data = extractor.get_neornithes_descendants()
    
    if not taxon_data:
        print("No Neornithes data found. Check your Fuseki dataset.")
        return
    
    # Create output file
    output_file = Path("../data/ontology/neornithes_extracted.owl")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create OWL file
    print(f"Creating OWL file with {len(taxon_data)} taxa...")
    triple_count, taxon_count = extractor.create_owl_file(output_file, taxon_data)
    
    print(f"\nExtraction complete!")
    print(f"Output file: {output_file}")
    print(f"Total triples: {triple_count:,}")
    print(f"Total taxa: {taxon_count:,}")
    print(f"File size: {output_file.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
