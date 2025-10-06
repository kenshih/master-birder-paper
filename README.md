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

## AviList/Avibase investigation: some takeaways

1. There are probably at least 2 tables that describe order. As well, this is suggested by the column "Sequence" in the original AviList 2025 Excel sheet. It could be described with tables Checklist(avibase_id, checklist_name, checklist_version, ..) -- e.g. checklist_name "AviList", version "2025"; and Sequence(checklist_id, avibase_id, seq_num, ..) -- where avibase_id is a taxon concept of a specific conscription found in, say, AviList 2025.
2. As suggested by the rubric/algorithm of inclusion, there are a number of things that are not self-descriptive about the database schema. There are likely a large number of rules in an application that populates the data that make the data work. The highly normalized structure means, when creating a "row" of, say, a new species, would require careful placement of a single avibaseID across several tables, across a number of dimensions of description. From this normalization, it's not quite clear, beyond reference to article literature, what makes for the conscription of the species. Perhaps other structures exist not described in the paper that do this -- though, it does seem to be extrinsic to, perhaps a precondition of, the data.
3. As far as the actual details are concerned, I'm not sure, I've captured the intended schema of the Avibase paper 100% correctly. So, this should be considered a "gist".

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
2. [`neorthines_uberon_relations.sparql`](./sparql/neorthines_uberon_relations.sparql) is a query demonstrating linkage of local data (local NBCI Taxon data) to another ontology, in this case to the "Uberon Multi-species Anatomy Ontology" (https://uberon.org/). Using our desired set (Aves) the resulting list shows mappings that exist in Uberon & the corresponding taxon name in NCBI Taxonomy, resulting in only 92 rows: [`neorthines_uberon_relations.csv`](./data/ontology/neorthines_uberon_relations.csv)
3. [`sample.uberon.detail.sparql`](./sparql/sample.uberon.detail.sparql) is a junky query just exploding out a sample of data that exists for anatomical parts in Uberon to illustrate what areas of discovery/traversal/information could be explored between Taxa and Anatomoy using these 2 datasets.
4. create dataset that maps avibase-id to ncbi-taxon-id 
    1. `sparql/select.ncbi-taxon-id-2-scientific-name.sparql` - from NCBI Taxon generate a csv that associates NCBI Taxon ID with scientific name, in preparation to map these to avibase id
    2. `notebooks/ontology_ncbitaxon.ipynb`
`sparql/create.ncbi-taxon-id-2-avibase-id.ttl` - load csv into new table in our local Avibase database.
    3. `generate_avibase_turtle.py` - to create turtle data to load into Fuseki.
        ```
        python generate_avibase_turtle.py data/avibase/master_birder.db sparql/avibase-instances.ttl
        ```
    4. load `avibase-instances.ttl` into Fuseki
    5. `sparql/sample.avibase2ncbi.sparql` - query shows association example query: `data/ontology/sample.avibase2ncbi.csv`
    ```
    "aviLabel","taxon","aviId","avidb_link"
    "Struthio molybdophanes","http://purl.obolibrary.org/obo/NCBITaxon_3150590","http://kenshih.com/master-birder/ontology#AvibaseID_avibase-40329BB6","https://avibase.bsc-eoc.org/species.jsp?avibaseid=avibase-40329BB6"
    "Struthio camelus","http://purl.obolibrary.org/obo/NCBITaxon_8801","http://kenshih.com/master-birder/ontology#AvibaseID_avibase-2247CB05","https://avibase.bsc-eoc.org/species.jsp?avibaseid=avibase-2247CB05"
    "Dromaius novaehollandiae","http://purl.obolibrary.org/obo/NCBITaxon_8790","http://kenshih.com/master-birder/ontology#AvibaseID_avibase-FD2456D5","https://avibase.bsc-eoc.org/species.jsp?avibaseid=avibase-FD2456D5"
    ...

    ```

## Ontology investigation: some takeaways

1. While, my first exercise of selecting the Avian subset from NCBI Taxonomy was a good exercise and an essential step in my in understanding the dataset, SPARQL, and Semantic Web workflow, in a real-world scenario this is an artificial step. Instead, I might start with my own dataset, map it to NCBI Taxonomy IDs, in order to unlock Uberon, GO, and other OBO Foundary biological datasets. For example, if my goal is to enrich AviList utility, I can simply map AviList IDs to NCBITaxon IDs. In hindsight, this is the exercise I could have run.
2. Uberon's finest-grain mapping between Avian taxa is at the Order-level, and here it has a total of only 5 mappings across only 2 orders e.g. "Strigiformes","feathered ear tuft" & "Passeriformes","area X of basal ganglion". Most of the rows simply correspond to class "Aves", with no representation of skeletal structures, such as the avian keel, coracoid bone, or furcula. I will read the Uberon paper to understand more & it may be I need to unpack the Uberon predicate definitions and usages; but in this surface treatment it seems that this coverage would be insufficient for focused or comparative studies of Avian life. For example, the Suliformes do not have external nares, absence of any unique beak structure representation for Suliformes suggests this description would need to come from somewhere else. What of birds that don't have a furcula? How about accounting for the albatross shoulder's lock-hinge? What about feather structures? I expect I'll find 2 things: 1) intent of Uberon is to capture components-only, not anatomical conscriptions for taxa; that should be provided per-taxa elsewhere 2) There are gaps for avian life. Gaps can be filled simply by anyone providing for an extension set of data for missing Avian taxa, since Semantic Web is AAA (anyone can say anything about anything).
    - Correction: Aves' "carina of sternum" is covered in Uberon as synonym of "keel"
    - After reading paper, aha, i get it. While there may be gaps and species work to do, Uberon is not meant so much for scAO (species anatomy ontologies) as an attempt at cross-taxa language describing anatomy independent of specific embodiment as much as possible.
3. The Uberon anatomy is extremely detailed. e.g. `Aves.telencephalic song nucleus HVC` `has part`s: "ectoderm-derived structure", "cellular anatomical entity", "atomic nucleus", "ectoderm-derived structure", "monoatomic monocation", "s-block molecular entity", etc totalling 54 `has_part` entities. In addition to `has_part`, 15 other relations exist, e.g. "causal agent in process", "developmentally preceded by", "mereotopologically related to", "has developmental contribution from", etc.

# Genetic investigation
    

## Unstructured Notes

- Anna's Hummingbird
    - https://avibase.bsc-eoc.org/species.jsp?avibaseid=42393721
        - avibase-42393721
        - TSN: 178036
- ncbitaxon.owl is 1.7G, so instead i trimmed it down to living Aves species-only -> ncbi_neornithes.owl
    - from https://jena.apache.org/download/
    - download apache-jena-fuseki-5.5.0.tar.gz
    - unpack and cd into it...
        ```
        # to start Fuseki, in dir or put on PATh
        ./fuseki-server
        # go to http://localhost:3030/#/ in browser for UI

        # in Fuseki CONSTRUCT query to create ncbi_neornithes.owl file (this was 0.ncbi_neornithes.owl)
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
break
```
Unexpected error making the query: GET https://stars-app.renci.org/ubergraph/sparql?query=SELECT++%2A%0AWHERE%0A++%7B+%7B+?uberon++%3Chttp://purl.obolibrary.org/obo/RO_0002162%3E++%3Chttp://purl.obolibrary.org/obo/NCBITaxon_100%3E+%3B%0A+++++++++++++++%3Chttp://www.w3.org/2000/01/rdf-schema%23label%3E++?uberonLabel%0A++++++OPTIONAL%0A++++++++%7B+%3Chttp://purl.obolibrary.org/obo/NCBITaxon_100%3E%0A++++++++++++++++++++%3Chttp://www.w3.org/2000/01/rdf-schema%23label%3E++?taxonLabel%0A++++++++%7D%0A++++%7D%0A++++FILTER+strstarts%28str%28?uberon%29%2C+%22http://purl.obolibrary.org/obo/UBERON_%22%29%0A++%7D%0A
```

```
# counting relation types
cat data/ontology/sample.uberon.detail.csv | grep "telencephalic song nucleus HVC" | cut -d, -f3 | sort | uniq 
```

1. to mock out as if my ontology was public
        ```
        # add to /etc/hosts
        127.0.0.1 kenshih.com
        # run web server
        pdm run site/web-server.py
        # was this needed?
        curl -X PUT -H "Content-Type: text/turtle" \
            --data-binary @index.ttl \
            "http://localhost:3030/birds?default"
        ```
    1. would need to put generated ttl into site/index.ttl
    2. need to make ontology#ref references work. 

## notes: Anna's Hummingbird

- https://avibase.bsc-eoc.org/species.jsp?avibaseid=42393721
    - avibase-42393721
    - TSN: 178036
