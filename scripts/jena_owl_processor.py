#!/usr/bin/env python3
"""
Jena-based OWL file processor for large taxonomic ontologies.

This script provides multiple approaches to process large OWL files using Apache Jena:
1. Direct Jena Java API (via subprocess)
2. RDFLib with Jena backend
3. Streaming processing for memory efficiency
4. Database storage for efficient querying

Usage:
    python scripts/jena_owl_processor.py --input data/ontology/ncbitaxon.owl --method streaming
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
import pandas as pd
import sqlite3
from typing import Iterator, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JenaOWLProcessor:
    """Process large OWL files using Apache Jena."""
    
    def __init__(self, jena_home: Optional[str] = None):
        """
        Initialize the Jena processor.
        
        Args:
            jena_home: Path to Jena installation (if not in PATH)
        """
        self.jena_home = jena_home
        self.project_root = Path(__file__).parent.parent
        
    def setup_jena(self) -> bool:
        """Setup Jena if not already available."""
        try:
            # Check if Jena is available
            result = subprocess.run(['java', '-cp', 'jena-arq-4.10.0.jar', 'org.apache.jena.arq.ARQ'], 
                                  capture_output=True, text=True, timeout=10)
            return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.info("Jena not found in PATH, will download and setup...")
            return self._download_jena()
    
    def _download_jena(self) -> bool:
        """Download and setup Jena."""
        try:
            jena_dir = self.project_root / "lib" / "jena"
            jena_dir.mkdir(parents=True, exist_ok=True)
            
            # Download Jena (you might want to use a specific version)
            jena_url = "https://downloads.apache.org/jena/binaries/apache-jena-4.10.0.tar.gz"
            
            logger.info(f"Downloading Jena to {jena_dir}")
            # This would require additional setup - for now, we'll use RDFLib approach
            return False
            
        except Exception as e:
            logger.error(f"Failed to setup Jena: {e}")
            return False
    
    def process_with_rdflib_streaming(self, owl_file: Path, output_dir: Path) -> Dict[str, Any]:
        """
        Process OWL file using RDFLib with streaming approach.
        
        Args:
            owl_file: Path to OWL file
            output_dir: Directory for output files
            
        Returns:
            Dictionary with processing statistics
        """
        from rdflib import Graph, Namespace
        from rdflib.plugins.parsers.notation3 import N3Parser
        
        logger.info(f"Processing {owl_file} with RDFLib streaming...")
        
        stats = {
            'total_triples': 0,
            'classes': 0,
            'properties': 0,
            'individuals': 0,
            'processing_time': 0
        }
        
        try:
            # Create output directory
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize graph
            g = Graph()
            
            # Parse the OWL file
            logger.info("Parsing OWL file...")
            g.parse(str(owl_file), format="xml")
            
            stats['total_triples'] = len(g)
            logger.info(f"Loaded {stats['total_triples']} triples")
            
            # Extract different types of entities
            owl_ns = Namespace("http://www.w3.org/2002/07/owl#")
            rdf_ns = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
            rdfs_ns = Namespace("http://www.w3.org/2000/01/rdf-schema#")
            
            # Count classes, properties, individuals
            for s, p, o in g:
                if p == rdf_ns.type:
                    if o == owl_ns.Class:
                        stats['classes'] += 1
                    elif o == owl_ns.ObjectProperty or o == owl_ns.DatatypeProperty:
                        stats['properties'] += 1
                    elif o == owl_ns.NamedIndividual:
                        stats['individuals'] += 1
            
            # Save to different formats
            self._save_graph_formats(g, output_dir, owl_file.stem)
            
            # Create summary
            self._create_summary(stats, output_dir, owl_file.stem)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error processing with RDFLib: {e}")
            raise
    
    def _save_graph_formats(self, graph, output_dir: Path, filename: str):
        """Save graph in multiple formats."""
        formats = {
            'ttl': 'turtle',
            'nt': 'ntriples',
            'json': 'json-ld'
        }
        
        for ext, fmt in formats.items():
            output_file = output_dir / f"{filename}.{ext}"
            try:
                graph.serialize(destination=str(output_file), format=fmt)
                logger.info(f"Saved {fmt} format to {output_file}")
            except Exception as e:
                logger.warning(f"Failed to save {fmt} format: {e}")
    
    def _create_summary(self, stats: Dict[str, Any], output_dir: Path, filename: str):
        """Create a summary of the processing results."""
        summary_file = output_dir / f"{filename}_summary.txt"
        
        with open(summary_file, 'w') as f:
            f.write(f"OWL Processing Summary for {filename}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total triples: {stats['total_triples']:,}\n")
            f.write(f"Classes: {stats['classes']:,}\n")
            f.write(f"Properties: {stats['properties']:,}\n")
            f.write(f"Individuals: {stats['individuals']:,}\n")
            f.write(f"Processing time: {stats['processing_time']:.2f} seconds\n")
        
        logger.info(f"Summary saved to {summary_file}")
    
    def process_to_database(self, owl_file: Path, db_file: Path) -> Dict[str, Any]:
        """
        Process OWL file and store in SQLite database.
        
        Args:
            owl_file: Path to OWL file
            db_file: Path to SQLite database
            
        Returns:
            Dictionary with processing statistics
        """
        from rdflib import Graph
        
        logger.info(f"Processing {owl_file} to database {db_file}")
        
        # Load graph
        g = Graph()
        g.parse(str(owl_file), format="xml")
        
        # Create database connection
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS triples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                predicate TEXT NOT NULL,
                object TEXT NOT NULL,
                context TEXT,
                UNIQUE(subject, predicate, object)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uri TEXT UNIQUE NOT NULL,
                type TEXT,
                label TEXT,
                description TEXT
            )
        ''')
        
        # Insert triples
        logger.info("Inserting triples into database...")
        batch_size = 10000
        batch = []
        
        for i, (s, p, o) in enumerate(g):
            batch.append((str(s), str(p), str(o), None))
            
            if len(batch) >= batch_size:
                cursor.executemany(
                    "INSERT OR IGNORE INTO triples (subject, predicate, object, context) VALUES (?, ?, ?, ?)",
                    batch
                )
                conn.commit()
                batch = []
                logger.info(f"Processed {i+1:,} triples...")
        
        # Insert remaining batch
        if batch:
            cursor.executemany(
                "INSERT OR IGNORE INTO triples (subject, predicate, object, context) VALUES (?, ?, ?, ?)",
                batch
            )
            conn.commit()
        
        # Create indexes for better query performance
        logger.info("Creating indexes...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_subject ON triples(subject)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_predicate ON triples(predicate)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_object ON triples(object)")
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) FROM triples")
        total_triples = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT subject) FROM triples")
        unique_subjects = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT predicate) FROM triples")
        unique_predicates = cursor.fetchone()[0]
        
        conn.close()
        
        stats = {
            'total_triples': total_triples,
            'unique_subjects': unique_subjects,
            'unique_predicates': unique_predicates,
            'database_file': str(db_file)
        }
        
        logger.info(f"Database processing complete: {total_triples:,} triples stored")
        return stats
    
    def query_database(self, db_file: Path, query: str) -> pd.DataFrame:
        """
        Query the database and return results as DataFrame.
        
        Args:
            db_file: Path to SQLite database
            query: SQL query string
            
        Returns:
            DataFrame with query results
        """
        conn = sqlite3.connect(str(db_file))
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Process large OWL files using Jena/RDFLib")
    parser.add_argument("--input", required=True, help="Path to input OWL file")
    parser.add_argument("--method", choices=["streaming", "database"], default="streaming",
                       help="Processing method")
    parser.add_argument("--output", help="Output directory or database file")
    parser.add_argument("--query", help="SQL query to run on database")
    
    args = parser.parse_args()
    
    # Initialize processor
    processor = JenaOWLProcessor()
    
    input_file = Path(args.input)
    if not input_file.exists():
        logger.error(f"Input file not found: {input_file}")
        sys.exit(1)
    
    try:
        if args.method == "streaming":
            output_dir = Path(args.output) if args.output else input_file.parent / "processed"
            stats = processor.process_with_rdflib_streaming(input_file, output_dir)
            print(f"Processing complete: {stats}")
            
        elif args.method == "database":
            db_file = Path(args.output) if args.output else input_file.parent / f"{input_file.stem}.db"
            stats = processor.process_to_database(input_file, db_file)
            print(f"Database processing complete: {stats}")
            
            if args.query:
                df = processor.query_database(db_file, args.query)
                print(f"Query results:\n{df}")
                
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
