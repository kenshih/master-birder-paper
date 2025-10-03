# master-birder-paper

```
pip install pdm
```

# AviList investigation

An investigation of AviList data through the exercise of creating and loading it into a simplified Avibase schema described the Avibase paper:

Lepage D, Vaidya G, Guralnick R (2014) Avibase – a database system for managing and organizing taxonomic concepts. ZooKeys 420: 117–135. doi: 10.3897/zookeys.420.7089

The goal is just to get a feel of the RDBMS representation and manipulation. While it would be most interesting to get a feel for how related but unequal circumscriptions relate (e.g. sensu lato vs. sensu stricto characterizations across lists in time); or, to simulate the 7-step process using the fractional weight algorithm to include and validate a checklist's incorporation into the db. In the interest of time, this investigation really just re-creates a baseline of data to play around with.

This simple exercise re-creates the database schema described in the Avibase paper, then takes the public list released by AviList (AviList 2025), transforms it and loads it into that database.

From there I was able to connect to it to run a number of queries just to explore what was there to exercise the mechanics involved in manipulating that data for query or a data application. (note data has been moved from data/ to data/avibase, so paths may need to be updated in notebooks)

1. `notebooks/avibase_db_setup.ipynb` - create database
2. `notebooks/avibase_load_data.ipynb` - clean avilist csv & load into db
3. `data/master_birder.db` - the resulting db
4. `data/AviList-v2025-11-extended.csv` - the raw avilist csv downloaded from https://www.avilist.org/
5. `data/AL25-*.csv` - working files derived from `AviList-v2025-11-extended.csv`,
   manipulated in `avibase_load_data.ipynb` 
6. `data/avibase.schema.mermaid` - my version of schema that came from the Avibase paper
7. `data/Problem.rows.csv` - 3 saved rows I removed that had errors, for expediency

## some takeaways

1. There are probably at least 2 tables that describe order. As well, this is suggested by the column "Sequence" in the original AviList 2025 Excel sheet. It could be described with tables Checklist(avibase_id, checklist_name, checklist_version, ..) -- e.g. checklist_name "AviList", version "2025"; and Sequence(checklist_id, avibase_id, seq_num, ..) -- where avibase_id is a taxon concept of a specific conscription found in, say, AviList 2025.
2. As suggested by the rubric/algorithm of inclusion, there are a number of things that are not self-descriptive about the database schema. There are likely a large number of rules in an application that populates the data that make the data work. The highly normalized structure means, when creating a "row" of, say, a new species, would require careful placement of a single avibaseID across several tables, across a number of dimensions of description. From this normalization, it's not quite clear, beyond reference to article literature, what makes for the conscription of the species. Perhaps other structures exist not described in the paper that do this -- though, it does seem to be extrinsic to, perhaps a precondition of, the data.

## notes: Anna's Hummingbird

- https://avibase.bsc-eoc.org/species.jsp?avibaseid=42393721
    - avibase-42393721
    - TSN: 178036

# Ontology investigation

1. `data/ontology/3.2.ncbi_neornithes_hier.owl` - NBCI Taxon of Neorthines queried out of large `ncbitaxon.owl` (not in repo) by using `sparql/neorthines_hier.sparql`. Experimented with Jena, Fuseki, ChatGPT, and Kepler AI. Final procedure:
    1. Downloaded NBCI Taxonomy from OBO Foundry
    2. Loaded it into local Fuseki Server tbd
    3. Developed CONSTRUCT query `sparql/neorthines_hier.sparql`
    4. Ran query in Fuseki and saved as `data/ontology/3.2.ncbi_neornithes_hier.owl`
    5. Also ran same query with command-line tool with `jena` instead of Fuseki, to take another timing: ~7s to build file
    6. Viewed file in Protégé
       ![In Protégé](./data/ontology/3.2.InProtege.png)
    In all this took several hours over a few days, to get a better feel for SPARQL, troubleshoot/evolve query, experiment.
    

## Notes

- ncbitaxon.owl is 1.7G, so instead i trimmed it down to living Aves species-only -> ncbi_neornithes.owl
    - from https://jena.apache.org/download/
    - download apache-jena-fuseki-5.5.0.tar.gz
    - unpack and cd into it...
        ```
        ./fuseki-server
        # go to http://localhost:3030/#/
        # in Fuseki CONSTRUCT query to create ncbi_neornithes.owl file
        PREFIX obo:        <http://purl.obolibrary.org/obo/>
        PREFIX ncbitaxon:  <http://purl.obolibrary.org/obo/ncbitaxon#>
        PREFIX rdfs:       <http://www.w3.org/2000/01/rdf-schema#>

        CONSTRUCT {
        ?cls ?p ?o .
        ?s ?pp ?cls .
        }
        WHERE {
        # species-level descendants of Neornithes (NCBITaxon:8825)
        ?cls rdfs:subClassOf+ obo:NCBITaxon_8825 ;
            ncbitaxon:has_rank obo:NCBITaxon_species .

        { ?cls ?p ?o }        # triples where the species is subject
        UNION
        { ?s ?pp ?cls }       # triples where the species is object
        }
        ```
- Fuseki was not returning so used: `apache-jena-5.5.0` client tools on fuseki `tbd`.
  ```
  source .env
  JAVA_TOOL_OPTIONS="-Xmx10g" tdb2.tdbquery --loc ../apache-jena-fuseki-5.5.0/run/databases/kendataset --query sparql/neorthines_with_parentage_lite.sparql > data/ontology/ncbi_neornithes_hier.ttl
  ```
  Even this light version didn't stop running after 1h of cpu time.
```
time JAVA_TOOL_OPTIONS="-Xmx10g" tdb2.tdbquery --loc ../apache-jena-fuseki-5.5.0/run/databases/kendataset --query sparql/neorthines_manually_created.sparql > data/ontology/ncbi_neornithes_hier.owl
107.65s user 11.20s system 109% cpu 1:48.79 total

time JAVA_TOOL_OPTIONS="-Xmx8g" tdb2.tdbquery --loc ../apache-jena-fuseki-5.5.0/run/databases/kendataset --query sparql/neorthines_hier.sparql > data/ontology/ncbi_neornithes_timing.owl
JAVA_TOOL_OPTIONS="-Xmx8g" tdb2.tdbquery --loc  --query  >   6.92s user 0.47s system 280% cpu 2.632 total
```
