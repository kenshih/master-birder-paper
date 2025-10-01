#!/usr/bin/env python3
"""
Load large OWL files into Apache Jena Fuseki for efficient querying.
"""

import requests
import time
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FusekiLoader:
    """Load OWL files into Fuseki server."""
    
    def __init__(self, fuseki_url="http://localhost:3030"):
        self.fuseki_url = fuseki_url
        self.admin_url = f"{fuseki_url}/$/datasets"
        
    def create_dataset(self, dataset_name, dataset_type="mem"):
        """Create a new dataset in Fuseki."""
        data = {
            "dbName": dataset_name,
            "dbType": dataset_type
        }
        
        try:
            response = requests.post(self.admin_url, data=data)
            if response.status_code == 200:
                logger.info(f"Created dataset: {dataset_name}")
                return True
            else:
                logger.error(f"Failed to create dataset: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error creating dataset: {e}")
            return False
    
    def load_owl_file(self, dataset_name, owl_file_path):
        """Load OWL file into Fuseki dataset."""
        upload_url = f"{self.fuseki_url}/{dataset_name}/data"
        
        try:
            with open(owl_file_path, 'rb') as f:
                files = {'file': f}
                data = {'graph': 'default'}
                
                logger.info(f"Uploading {owl_file_path} to {dataset_name}...")
                response = requests.post(upload_url, files=files, data=data)
                
                if response.status_code == 200:
                    logger.info(f"Successfully loaded {owl_file_path}")
                    return True
                else:
                    logger.error(f"Upload failed: {response.status_code}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            return False
    
    def query_dataset(self, dataset_name, sparql_query):
        """Execute SPARQL query on dataset."""
        query_url = f"{self.fuseki_url}/{dataset_name}/sparql"
        
        try:
            response = requests.get(query_url, params={'query': sparql_query})
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Query failed: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return None

def main():
    """Load NCBI taxonomy into Fuseki."""
    
    # Initialize Fuseki loader
    fuseki = FusekiLoader()
    
    # File paths
    project_root = Path(__file__).parent.parent
    ncbi_file = project_root / "data" / "ontology" / "ncbitaxon.owl"
    
    if not ncbi_file.exists():
        print(f"NCBI file not found: {ncbi_file}")
        return
    
    # Check if Fuseki is running
    try:
        response = requests.get(fuseki.fuseki_url, timeout=5)
        if response.status_code != 200:
            print("Fuseki server not running. Please start it first:")
            print("  cd apache-jena-fuseki-5.5.0")
            print("  ./fuseki-server")
            return
    except:
        print("Cannot connect to Fuseki server. Please start it first:")
        print("  cd apache-jena-fuseki-5.5.0")
        print("  ./fuseki-server")
        return
    
    # Create dataset
    dataset_name = "ncbitaxon"
    if not fuseki.create_dataset(dataset_name):
        print("Failed to create dataset")
        return
    
    # Load OWL file
    print(f"Loading {ncbi_file.name} into Fuseki...")
    print("This may take several minutes for large files...")
    
    start_time = time.time()
    if fuseki.load_owl_file(dataset_name, ncbi_file):
        load_time = time.time() - start_time
        print(f"Successfully loaded in {load_time:.1f} seconds")
        
        # Test query
        test_query = """
        SELECT (COUNT(*) as ?count)
        WHERE {
            ?s ?p ?o .
        }
        """
        
        result = fuseki.query_dataset(dataset_name, test_query)
        if result:
            count = result['results']['bindings'][0]['count']['value']
            print(f"Dataset contains {count} triples")
        
        print(f"\nAccess your data at: http://localhost:3030/{dataset_name}/sparql")
        print("\nSample queries:")
        print("1. Find taxonomic ranks:")
        print("   SELECT ?rank (COUNT(*) as ?count) WHERE { ?taxon <http://purl.obolibrary.org/obo/NCBITaxon_rank> ?rank } GROUP BY ?rank ORDER BY DESC(?count) LIMIT 10")
        
        print("\n2. Find bird taxa:")
        print("   SELECT ?taxon ?label WHERE { ?taxon <http://www.w3.org/2000/01/rdf-schema#label> ?label . FILTER(CONTAINS(LCASE(?label), \"bird\")) } LIMIT 10")
    else:
        print("Failed to load OWL file")

if __name__ == "__main__":
    main()
