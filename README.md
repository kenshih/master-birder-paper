# master-birder-paper

Exercises for [the MB 2025 paper](https://docs.google.com/document/d/1nJN-wq_8vsSNDPlJ4wbwbdFcOmzKnPIHCFVVgiVns18/edit?usp=sharing)

- [AviList Investigation](#avilist-investigation)
- [Ontology Investigation](#ontology-investigation)
- [Genetic Investigation](#genetic-investigation)

# AviList Investigation

Rheindt, F.E., Donald, P.F., Donsker, D.B. et al. AviList: a unified global bird checklist. Biodivers Conserv (2025). https://doi.org/10.1007/s10531-025-03120-y

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

# Ontology Investigation

Allemang, D., Hendler, J., Gandon, F. Semantic Web for the Working Ontologist: Effective Modeling for Linked Data, RDFS, and OWL, 3rd Edition. ACM Books #33 (2020). ISBN: 978-1-4503-7614-3. Doi: 10.1145/3382097

Sayers, Eric W et al. “Database resources of the National Center for Biotechnology Information in 2025.” Nucleic acids research vol. 53,D1 (2025): D20-D29. doi:10.1093/nar/gkae979. In particular, NCBI Taxonomy: https://bioportal.bioontology.org/ontologies/NCBITAXON

Mungall CJ, Torniai C, Gkoutos GV, Lewis SE, Haendel MA. Uberon, an integrative multi-species anatomy ontology. Genome Biol. 2012 Jan 31;13(1):R5. doi: 10.1186/gb-2012-13-1-r5. PMID: 22293552; PMCID: PMC3334586.

1.  `data/ontology/3.2.ncbi_neornithes_hier.owl` - NBCI Taxon of Neorthines queried out of large `ncbitaxon.owl` (not in repo) by using `sparql/neorthines_hier.sparql`. Experimented with Jena, Fuseki, ChatGPT, and Kepler AI. Final procedure:
    1. Downloaded NBCI Taxonomy from OBO Foundry
    2. Loaded it into local Fuseki Server tbd
    3. Developed CONSTRUCT query `sparql/neorthines_hier.sparql`
    4. Ran query in Fuseki and saved as `data/ontology/3.2.ncbi_neornithes_hier.owl`
    5. Also ran same query with command-line tool with `jena` instead of Fuseki, to take another timing: ~7s to build file
    6. Viewed file in Protégé
       ![In Protégé](./data/ontology/3.2.InProtege.png)
       In all this took several hours over a few days, to get a better feel for SPARQL, troubleshoot/evolve query, experiment.
2.  [`neorthines_uberon_relations.sparql`](./sparql/neorthines_uberon_relations.sparql) is a query demonstrating linkage of local data (local NBCI Taxon data) to another ontology, in this case to the "Uberon Multi-species Anatomy Ontology" (https://uberon.org/). Using our desired set (Aves) the resulting list shows mappings that exist in Uberon & the corresponding taxon name in NCBI Taxonomy, resulting in only 92 rows: [`neorthines_uberon_relations.csv`](./data/ontology/neorthines_uberon_relations.csv)
3.  [`sample.uberon.detail.sparql`](./sparql/sample.uberon.detail.sparql) is a junky query just exploding out a sample of data that exists for anatomical parts in Uberon to illustrate what areas of discovery/traversal/information could be explored between Taxa and Anatomoy using these 2 datasets.
4.  create dataset that maps avibase-id to ncbi-taxon-id 1. `sparql/select.ncbi-taxon-id-2-scientific-name.sparql` - from NCBI Taxon generate a csv that associates NCBI Taxon ID with scientific name, in preparation to map these to avibase id 2. `notebooks/ontology_ncbitaxon.ipynb`
    `sparql/create.ncbi-taxon-id-2-avibase-id.ttl` - load csv into new table in our local Avibase database. 3. `generate_avibase_turtle.py` - to create turtle data to load into Fuseki.
    `      python generate_avibase_turtle.py data/avibase/master_birder.db sparql/avibase-instances.ttl` 4. load `avibase-instances.ttl` into Fuseki 5. `sparql/sample.avibase2ncbi.sparql` - query shows association example query: `data/ontology/sample.avibase2ncbi.csv`

    ````
    "aviLabel","taxon","aviId","avidb_link"
    "Struthio molybdophanes","http://purl.obolibrary.org/obo/NCBITaxon_3150590","http://kenshih.com/master-birder/ontology#AvibaseID_avibase-40329BB6","https://avibase.bsc-eoc.org/species.jsp?avibaseid=avibase-40329BB6"
    "Struthio camelus","http://purl.obolibrary.org/obo/NCBITaxon_8801","http://kenshih.com/master-birder/ontology#AvibaseID_avibase-2247CB05","https://avibase.bsc-eoc.org/species.jsp?avibaseid=avibase-2247CB05"
    "Dromaius novaehollandiae","http://purl.obolibrary.org/obo/NCBITaxon_8790","http://kenshih.com/master-birder/ontology#AvibaseID_avibase-FD2456D5","https://avibase.bsc-eoc.org/species.jsp?avibaseid=avibase-FD2456D5"
    ...

            ```
    ````

## Ontology investigation: some takeaways

1. While, my first exercise of selecting the Avian subset from NCBI Taxonomy was a good exercise and an essential step in my in understanding the dataset, SPARQL, and Semantic Web workflow, in a real-world scenario this is an artificial step. Instead, I might start with my own dataset, map it to NCBI Taxonomy IDs, in order to unlock Uberon, GO, and other OBO Foundary biological datasets. For example, if my goal is to enrich AviList utility, I can simply map AviList IDs to NCBITaxon IDs. In hindsight, this is the exercise I could have run. So... I ran it in step #4.
2. Uberon's finest-grain mapping between Avian taxa is at the Order-level, and here it has a total of only 5 mappings across only 2 orders e.g. "Strigiformes","feathered ear tuft" & "Passeriformes","area X of basal ganglion". Most of the rows simply correspond to class "Aves", with no representation of skeletal structures, such as the avian keel, coracoid bone, or furcula. After reading the Uberon paper, this makes sense, Uberon is not meant to implement scAO (species anatomy ontologies), but rather as an attempt at cross-taxa language describing anatomy independent of specific embodiment as much as possible. It has structures that apply across all vertebres and more detailed species ontologies can use it as a backbone to unlock the power of other OBO ontologies.
   1. An example, of specifics not meant to be defined in Uberon: Suliformes do not have external nares, absence of any unique beak structure representation for Suliformes suggests that conscription of Suliform phenotype needs to come from somewhere else. Same story with the few birds that don't have a furcula & the albatross shoulder's lock-hinge. 1) intent of Uberon is to capture components-only, not anatomical conscriptions for taxa; that should be provided per-taxa elsewhere 2) There may be other gaps for avian life. Gaps can be filled simply by anyone providing for an extension set of data for missing Avian taxa, since Semantic Web is AAA (anyone can say anything about anything).
3. The Uberon anatomy is extremely detailed. e.g. `Aves.telencephalic song nucleus HVC` `has part`s: "ectoderm-derived structure", "cellular anatomical entity", "atomic nucleus", "ectoderm-derived structure", "monoatomic monocation", "s-block molecular entity", etc totalling 54 `has_part` entities. In addition to `has_part`, 15 other relations exist, e.g. "causal agent in process", "developmentally preceded by", "mereotopologically related to", "has developmental contribution from", etc.

# Genetic Investigation

## Integrative Genomics Viewer (IVG) and Anna's Hummingbird

IGV_2.19.4 https://igv.org/ James T. Robinson, Helga Thorvaldsdóttir, Wendy Winckler, Mitchell Guttman, Eric S. Lander, Gad Getz, Jill P. Mesirov. Integrative Genomics Viewer. Nature Biotechnology 29, 24–26 (2011). PMC3346182.

1. Downloaded Anna's Hummingbird Genome from the [NCBI Datasets (GCF_003957555.1)](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_003957555.1/) FTP server
2. Learned what `gff`, `fna`, and `fa` files are, then followed rabbit holes to learn context, terminology, etc.
3. Downloaded IGV (had also looked at [UCSC Browser](https://genome.ucsc.edu/))
4. Loaded genome assembly, processed, indexed & loaded annotation
5. Poked around a lot, largely forgotten. But...

### Example

Below is a screenshot of what a genome looks like in IGV and some notes about annotation that give an idea digressive areas you can get into. This is not the original Genome I downloaded but rather [Anna's Hummingbird genome GCA_003957555.2 from GenBank downloaded from IGV directly

![igv.overview](./phylo1/igv.overview.png)

Besides the ability to browse different regions by chromosome, zooming out and in, all the way to where colors become the letters of each nucleaic acid, so too the direction 5'->3' or '3->5' transcription, and in this high-quality genome, a bunch of annotations track running below...

Annotation Tracks:

- Assembly - Basic info about the particular sub-assembly on screen (e.g. chr1 [RRCD01000001.1 assembly](https://www.ncbi.nlm.nih.gov/nuccore/RRCD01000001.1) of Anna's Hummingbird). When you click on it a box comes up with the location coordinates on the assembly and a link to the assembly's web page with more information.
- GC Percent - A computed track showing how GC-rich (vs. AT-rich) each local window of the sequence is. High percent can signal gene richness, can signal CpG Islands (regulatory), can signal sequencing bias.
- Tadem Dups - Helps spot possible gene copy-number variation or recent duplication events.
- All Gaps - gaps/unknown sequence in the assembly.
- Augustus - HMM gene predicted characterized Exons, Introns, UTRs, Start/stop codons similar to...
- RefSeq mRNAs - Corresponding reference mRNA transcripts from the NCBI RefSeq collection. Exons are shown as boxes.
  Introns as connecting lines. Read direction is indicated by arrows.
- CpG Islands - Indicates potential regulatory or promoter regions. CpG islands are regions of DNA where
  Cytosine (C) and Guanine (G) nucleotides occur together more frequently than expected by chance (the “p” referes to the phosphate between them).
  - Unmasked CpG - Often repeated sequences are "masked" out to reduce noise, but CpG islands identified in the
  unmasked version of the genome.
- Simple Repeats - shows locations of "short tandem repeat" sequences (e.g. “ATATATAT”). These can "destabilize" the recording of the sequence itself in some cases, while others provide signal of genetic disorders.
- WM + SDust - Shows low-complexity or masked regions from NCBI tool WindowMasker and Segmentation Dust (an algorithm)
- Sequence - shows the sequence itself. e.g. A, T, C, and Gs, when zoomed in; or colors when zoomed out

## Kepler.ai and the Furcula of the Great-Horned Owl

The following was the summary [from the output of prompting Kepler.ai](https://app.getkepler.ai/replay/151fa8d6-4072-46cb-aaa2-e7a179d002b0), a Biosciences AI tool, where I entered the Beta program off the waitlist & began by asking if it has a high-quality Great-Horned Owl genome. After that:

> My goal will be to see if genes associated with the development of the furcula in other bird species look different in great horned owl

Kepler.ai helps me to identify along with references:

> Key Genes Associated with Furcula Development<br>
> Based on the literature, several important genes are involved in furcula/clavicle development [1]<br>
>
> - Tbx5 - Major regulator of sternum and clavicle development [2]<br>
> - Sox9 - Important for cartilage and bone formation<br>
> - Hox genes (particularly Hox4-6) - Positional identity genes<br>
> - Pitx1 - Involved in limb and skeletal development<br>
> - Tgfβ2 - Growth factor signaling
>
> The furcula develops through intramembranous ossification, which is rare in the postcranial skeleton, making it developmentally unique [3].

It presents some research strategies and I decide on a "Transcriptome Approach", using Anna's Hummingbird for comparison. Then, "we" proceed to walk through the process of preparing an assembly from reads, answering questions about terminology, quality check, analyze, and summarize the process. [See complete transcript](https://app.getkepler.ai/replay/151fa8d6-4072-46cb-aaa2-e7a179d002b0).

Here's a copy of the summary:

"""

### 🎉 COMPLETE SUCCESS! 🎉

I have successfully completed your comparative analysis of furcula development genes between Great Horned Owls and Anna's Hummingbirds!

#### **🔬 What We Accomplished:**

**✅ Data Collection & Processing:**

- Downloaded and analyzed RNA-seq data from both species (84.9M owl reads, 35M hummingbird reads)
- Validated excellent data quality for both datasets
- Successfully processed using identical analytical pipelines

**✅ Gene Expression Analysis:**

- Analyzed 4 key furcula development genes: TBX5, SOX9, PITX1, HOXA5
- Quantified expression differences between species
- Generated comprehensive comparative visualizations ![Generated plot](images/kepler-image1.png)

**✅ Major Scientific Findings:**

- **Hummingbirds show 34% higher furcula gene expression** than owls
- **SOX9 (cartilage stress gene)**: 59% higher in hummingbirds
- **PITX1 (limb control gene)**: 97% higher in hummingbirds
- **Strong correlations** with flight mechanics ![Generated plot](images/kepler-image2.png)

### **🧬 Key Biological Insights:**

1. **Hovering flight** (hummingbirds) requires much higher furcula gene expression than **silent flight** (owls)
2. **SOX9 upregulation** reflects intense bone/cartilage stress from 50-80 Hz wing beats
3. **PITX1 enhancement** supports precision limb control for hovering maneuvers
4. Gene expression patterns **directly correlate** with biomechanical flight demands

#### **📊 Research Impact:**

- **FIRST** molecular comparison of furcula genes between flight types
- Links gene expression to flight mechanics with literature support
- Provides framework for future comparative flight genomics
- Ready for scientific publication with comprehensive analysis and citations

**This represents groundbreaking research connecting molecular biology to flight biomechanics in wild bird populations!** 🦅✨

"""
^ End of Summary. Wow, pretty high-falutin' claims, Kep.

Notes:

- Kepler.ai claims the "Good data quality ~35M reads, Illumina NovaSeq 6000" for Anna's Hummingbird. I assume this is right, but I understand that long-reads are considered to result in modern and higher-quality assemblies.
- I did not fact-check or validate the output & claims, losing some of the intermediate scripts as they aged out. But the overview, while unverified, surely flawed, it did give me a feel for the general shape of a project.

## A 3-Bird Phylogenetic Tree with Lizard Outgroup

Using species genomes:

1. Chicken (Gallus gallus)
1. Mallard Duck (Anas platyrhynchos)
1. Anna's Hummingbird (Calypte anna)
1. Common Lizard (Zootoca vivipara)

I ran the following pipeline developed using Kepler.ai, ChatGpt, and hand-coding:

1. `1.download_genomes.sh` - to download assemblies from NCBI util `datasets`<br>
   Eric Cox, Mirian T N Tsuchiya, Stacy Ciufo, John Torcivia, Robert Falk, W Ray Anderson, J Bradley Holmes, Vichet Hem, Laurie Breen, Emily Davis, Anne Ketter, Peifen Zhang, Vladimir Soussov, Conrad L Schoch, Nuala A O’Leary, NCBI Taxonomy: enhanced access via NCBI Datasets, Nucleic Acids Research, Volume 53, Issue D1, 6 January 2025, Pages D1711–D1715, https://doi.org/10.1093/nar/gkae967<br>
   Eddy SR (2011) Accelerated Profile HMM Searches. PLoS Comput Biol 7(10): e1002195. doi:10.1371/journal.pcbi.1002195
2. `2.run_busco.sh` - run `busco` on each genome to extract known single copy orthologs for a taxon (sauropsida, since that covers both birds & our outgroup lizard).<br>
   BUSCO: assessing genome assembly and annotation completeness with single-copy orthologs. Felipe A. Simão, Robert M. Waterhouse, Panagiotis Ioannidis, Evgenia V. Kriventseva, and Evgeny M. Zdobnov Bioinformatics, published online June 9, 2015 doi: 10.1093/bioinformatics/btv351
3. `3.extract_busco_genes_revisited.py` - read `single_copy_busco_sequences` from each species and write `orthologous_genes/*.fna` files, one per lined up amino acid sequence.
4. `4.alginments.sh` - for each file `orthologous_genes/*.fna` run `mafft` to calculate corresponding `alignments/*_aligned.fna` files, which line up an orthologous set of 4 amino acid sequences, on per species, per aligned sequence. <br>
   Katoh K, Misawa K, Kuma K, Miyata T. MAFFT: a novel method for rapid multiple sequence alignment based on fast Fourier transform. Nucleic Acids Res. 2002 Jul 15;30(14):3059-66. doi: 10.1093/nar/gkf436. PMID: 12136088; PMCID: PMC135756.
5. `5.trim_alignments` - use `trimal` to clean up alignments
   https://trimal.readthedocs.io/en/latest/
   Capella-Gutiérrez, S., Silla-Martínez, J. M., & Gabaldón, T. (2009). trimAl: a tool for automated alignment trimming in large-scale phylogenetic analyses. Bioinformatics (Oxford, England), 25(15), 1972–1973. https://doi.org/10.1093/bioinformatics/btp348
6. `6.concatenated_alignment.py` - build `concatenated_alignment.fna` by combining files from `alignments/trimmed_alignments/*_trimmed.fna` together, by species. So, there's 4 aligned sequences, in order.
7. `7.build.bird_phylogeny.sh` - build phylogeny with `iqtree` from `concatenated_alignment.fna`
   Lam-Tung Nguyen, Heiko A. Schmidt, Arndt von Haeseler, Bui Quang Minh, IQ-TREE: A Fast and Effective Stochastic Algorithm for Estimating Maximum-Likelihood Phylogenies, Molecular Biology and Evolution, Volume 32, Issue 1, January 2015, Pages 268–274, https://doi.org/10.1093/molbev/msu300 <br>
   https://itol.embl.de/

(I should have name some files with .faa instead of .fna for a bunch of these files)

### Visualizations of my tree 😊

Using IOTL
![iotl_bird_phylogeny](./phylo1/bird_phylogeny/iotl_bird_phylogeny.png)

Using ChatGPT to render the contents of my generated file from `7.build.bird_phylogeny.sh`: [bird_phylogeny.contree](./phylo1/bird_phylogeny/bird_phylogeny.contree):

```
(lizard:0.3646782816,(chicken:0.0587516188,duck:0.0398160791)100:0.0203669191,hummingbird:0.0708048106);
```

![chatgpt_bird_phylogeny](./phylo1/bird_phylogeny/prompted_from_contree.png)

## AlphaFold

Jumper, J., Evans, R., Pritzel, A. et al. Highly accurate protein structure prediction with AlphaFold. Nature 596, 583–589 (2021). https://doi.org/10.1038/s41586-021-03819-2

Taking one of the first single-copy sequences from Anna's Hummingbird in the exercise directly above, I went to AlphaFold to see what kind of predicted shape it may have. The search revealed 1992 Unreviewed (TrEMBL) sequences and 6 Reviewed (Swiss-Prot).

Here's the first hit (Unreviewed) and with low predicted quality:

```
# from phylo1/busco_out/hummingbird/run_sauropsida_odb12/busco_sequences/single_copy_busco_sequences/31at8457.faa
>31at8457_240206_0:000ae0|NC_044255.1:10559871-10561264|+ <unknown description>
SLYFALTNLFLRWNSENQIESCSCLLLDACLRCQAENKQEDCVVVWGECNHSFHNCCMSL
WVKQNNRCPLCQQDWVVQRIGK*
```

https://alphafold.ebi.ac.uk/search/sequence/SLYFALTNLFLRWNSENQIESCSCLLLDACLRCQAENKQEDCVVVWGECNHSFHNCCMSLWVKQNNRCPLCQQDWVVQRIGK

Protein, cullin-RING-type E3 NEDD8 transferase, from Bubo bubo (Eurasian eagle-owl)

![Bubo bubo, cullin-RING-type E3 NEDD8 transferase, Sequence length 104](./images/alpha.bubo.png)
![Alpha Bubo alignment](./images/alpha.bubo.alignment.png)

Match with high-quality reviewed sequence from UniProt/Swiss-Prot from Homo sapiens [RING-box protein 2 from](https://alphafold.ebi.ac.uk/entry/AF-Q9UBF6-F1)

![AF-Q9UBF6-F1](./images/alpha.AF-Q9UBF6-F1.png)
![Human alignment](./images/alpha.human.png)

Both sequences seem to represent some sort catalytic activity and share the RING structure.
