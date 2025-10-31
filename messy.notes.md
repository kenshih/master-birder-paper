## Unstructured Notes

```
pip install pdm
```

# trying to switch to compleasm, since mamba install failed

git clone https://github.com/huangnengCSU/compleasm.git
cd compleasm

# go into phylo venv and install compleasm locally

cd /Users/ken/Documents/wk/master-birder-paper && mamba run -n phylo pip install ../compleasm/

cd /Users/ken/Documents/wk/master-birder-paper && mamba run -n phylo conda install -c bioconda miniprot hmmer -y

find /Users/ken/Documents/wk/master-birder-paper/phylo1/genomes -name "\*.fna" -type f

cd /Users/ken/Documents/wk/master-birder-paper/phylo1 && mamba run -n phylo compleasm download sauropsida_odb12

```

```

# use to sanity check: what species am i looking at?

datasets summary genome accession GCF_000344595.1 | jq '.reports[0] | {organism_name: .organism.organism_name, common_name: .organism.common_name, accession}'

```

```

## will add this to my set in meantime

```
datasets download genome accession GCA_002880195.1 --filename genomes/owl_genome.zip

```

### orig genome notes

```
# mamba
brew install miniforge
amba create -n phylo -c conda-forge -c bioconda python=3.11 iqtree mafft trimal ncbi-datasets-cli -y

eval "$(mamba shell hook --shell zsh)"
To automatically initialize all future (zsh) shells, run:
    $ mamba shell init --shell zsh --root-prefix=~/.local/share/mamba
mamba activate phylo
```

- run `phylo1/1.download_genomes.sh`

```
conda install numpy # (in phylo -n)
docker pull ezlabgva/busco:v6.0.0_cv1
docker run --rm -it --platform linux/amd64 ezlabgva/busco:v6.0.0_cv1 busco -v
docker run --rm -it --platform linux/amd64 -v "$PWD":/data -w /data ezlabgva/busco:v6.0.0_cv1 busco -h

alias busco='docker run --rm -it --platform linux/amd64 -v "$PWD":/data -w /data ezlabgva/busco:v6.0.0_cv1 busco'

busco --list-datasets

busco -i genomes/chicken_genome/ncbi_dataset/data/
GCF_000002315.5/GCF_000002315.5_GRCg6a_genomic.fna  -l aves_odb12 -o chicken_busco -m genome --cpu 4
# failed with out of resources
busco -i genomes/chicken_genome/ncbi_dataset/data/GCF_000002315.5/GCF_000002315.5_GRCg6a_genomic.fna -l aves_odb12 -o chicken_busco -m genome --cpu 2 -f
...

 24K    alligator_busco
3.8G    busco_downloads
828K    busco.output.png
3.4G    chicken_busco
3.5G    duck_busco
6.7G    genomes
3.5G    hummingbird_busco
4.0K    sourceme
 24K    turtle_busco
2.1G    turtle_genome
652M    turtle_genome.zip

> mamba install pathlib
> python 3.extract_busco_genes.py
Successfully extracted 5963 orthologous genes!
Gene files saved in: orthologous_genes
./4.alignments.sh
./5.trim_alignments.sh > 5.trim_alignments.OUT 2>&1 &
python 6.concatenated_alignment.py > 6.concatenated_alignment.OUT 2>&1
# creates a file called "concatenated_alignment.fna"
./7.build.bird_phylogeny.sh > 7.build.bird_phylogeny.OUT 2>&1 &
# this failed because i'm only doing 3 species
# so trying this, just to get to the end while i clean up
iqtree -s concatenated_alignment.fna -m MFP -nt AUTO --prefix bird_3species
# results in this tree: (duck:0.039350353,chicken:0.056465082,hummingbird:0.1063995);
```

in https://itol.embl.de/
![itol](phylo1/itol.3-species.png)

## Issues

- [ ] anna's wrong assembly (was zebra finch)
- [ ] mallard wrong assembly (was pink-footed goose)


## needed to correct this mistake

(phylo) ➜ phylo1 git:(main) ✗ datasets summary genome accession GCF_003957555.1 | jq '.reports[0] | {organism_name: .organism.organism_name, common_name: .organism.common_name, accession}'
{
"organism_name": "Calypte anna",
"common_name": "Anna's hummingbird",
"accession": "GCF_003957555.1"
}
(phylo) ➜ phylo1 git:(main) ✗ datasets summary genome accession GCA_003957565.1 | jq '.reports[0] | {organism_name: .organism.organism_name, common_name: .organism.common_name, accession}'
{
"organism_name": "Taeniopygia guttata",
"common_name": "zebra finch",
"accession": "GCA_003957565.1"
}

###

✗ cat alignments/trimmed_alignments/99952at8782_trimmed.fna

> chicken
> MAISNVRYGEGVTKEIGMDLQNLGAKRVCLMTDRNLSQLPPVDAVLNSLTKSGINFQMYD
> NVRVEPTDQSFLDAIEFAKKGEFDAYVAVGGGSVIDTCKAANLYASSPTSDFLDYVNAPI
> GKGKAVTVPLKPLIAVPTTAGTGSETTGVAIFDFKELKVKTGIASRAIKPTLGIIDPLHT
> LSMPERIVANSGFDVLCHALESYTALPYKMRSPCPSNPINRPAYQGSNPISDVWALHALR
> IVAKYLKRAIRNPEDREARANMHLASAFAGIGFGNAGVHLCHGMSYPISGLVKTYKPKDY
> NVDHSLVPHGLSVVLTSPAVFAFTAQVHPERHLEAAEILGADIRTARIKDAGLILADTLR
> KFLFDLNVDDGLAAIGYSKADIPALVKGTLPQERVTKLSPRPQTEEDLSALFEASMKLY
> hummingbird
> MAISNIRYGEGVTKEIGMDLQNLGARRVCLMTDKNLSKLPPVNAVLNSLAKYGINFQMYD
> NVRVEPTDQSFLDAIQFAKKGEFDAYVAVGGGSVIDTCKAANLYAASPSSEFLDYVNAPI
> GKGKPVTVPLKPLIAVPTTSGTGSETTGVAIFDFKELKVKTGIASRAIKPTLGIIDPLHT
> LSMPERIVANSGFDVLCHALESYTALPYNQRCPCPSNPINRPAYQGSNPVSDVWALHALR
> IVAKYLKRAIRNPEDHEARANMHLASAFAGIGFGNAGVHLCHGMSYPISGLVKTYKPKDY
> NVDHSLVPHGLSVVLTSPAVFAFTAQIHPERHLEAAEILGADIRTARIKDAGLILADTLR
> KFLFDLNVDDGLAAIGYSKADIPALVKGTLPQERVTKLSPRPQTEEDLSALFEASMKLY
> duck
> MAVSNIRYGEGVTKEIGMDLKNLGAQRVCLMTDKNLSQLPPVNAVLNSLAKYGVNFQMYD
> EVRVEPTDQSFLHAIEFAKKGEFDAYVAVGGGSVIDTCKAANLYASSPTSDFLDYVNAPI
> GKGKPVTVPLKPHIAVPTTAGTGSETTGVAIFDFKELKVKTGIASRAIKPTLGIIDPLHT
> LSMPERIVANSGFDVLCHALESYTALPYKMRSPCPSNPINRPAYQGSNPISDIWALHALR
> IVAKYLKRAIRNPEDREARANMHLASAFAGIGFGNAGVHLCHGMSYPISGLVKTYKPKDY
> NVDHSLVPHGLSVVLTSPAVFAFTAQVHPERHLEAAEILGADIRTARIKDAGFILADTLR
> KFLFDLNVDDGLAAIGYSKADIPALVKGTLPQERVTKLSPRPQTEEDLSALFEASMKLY

(phylo) ➜ phylo1 git:(main) ✗ cat alignments/99952at8782_aligned.fna

> chicken
> ----------------------------------------------MAISNVRYGEGVTK
> EIGMDLQNLGAKRVCLMTDRNLSQLPPVDAVLNSLTKSGINFQMYDNVRVEPTDQSFLDA
> IEFAKKGEFDAYVAVGGGSVIDTCKAANLYASSPTSDFLDYVNAPIGKGKAVTVPLKPLI
> AVPTTAGTGSETTGVAIFDFKELKVKTGIASRAIKPTLGIIDPLHTLSMPERIVANSGFD
> VLCHALESYTALPYKMRSPCPSNPINRPAYQGSNPISDVWALHALRIVAKYLKRAIRNPE
> DREARANMHLASAFAGIGFGNAGVHLCHGMSYPISGLVKTYKPKDYNVDHSLVPHGLSVV
> LTSPAVFAFTAQVHPERHLEAAEILGADIRTARIKDAGLILADTLRKFLFDLNVDDGLAA
> IGYSKADIPALVKGTLPQERVTKLSPRPQTEEDLSALFEASMKLY
> hummingbird
> MAAGRARVSRLLRLLQRAACRCPSHGHTYSQVPEQPNLGNTDYAFEMAISNIRYGEGVTK
> EIGMDLQNLGARRVCLMTDKNLSKLPPVNAVLNSLAKYGINFQMYDNVRVEPTDQSFLDA
> IQFAKKGEFDAYVAVGGGSVIDTCKAANLYAASPSSEFLDYVNAPIGKGKPVTVPLKPLI
> AVPTTSGTGSETTGVAIFDFKELKVKTGIASRAIKPTLGIIDPLHTLSMPERIVANSGFD
> VLCHALESYTALPYNQRCPCPSNPINRPAYQGSNPVSDVWALHALRIVAKYLKRAIRNPE
> DHEARANMHLASAFAGIGFGNAGVHLCHGMSYPISGLVKTYKPKDYNVDHSLVPHGLSVV
> LTSPAVFAFTAQIHPERHLEAAEILGADIRTARIKDAGLILADTLRKFLFDLNVDDGLAA
> IGYSKADIPALVKGTLPQERVTKLSPRPQTEEDLSALFEASMKLY
> duck
> MAAGRERAARLLRQLQRAACRCPSHCHTYSRVPEHATLGNTDYAFEMAVSNIRYGEGVTK
> EIGMDLKNLGAQRVCLMTDKNLSQLPPVNAVLNSLAKYGVNFQMYDEVRVEPTDQSFLHA
> IEFAKKGEFDAYVAVGGGSVIDTCKAANLYASSPTSDFLDYVNAPIGKGKPVTVPLKPHI
> AVPTTAGTGSETTGVAIFDFKELKVKTGIASRAIKPTLGIIDPLHTLSMPERIVANSGFD
> VLCHALESYTALPYKMRSPCPSNPINRPAYQGSNPISDIWALHALRIVAKYLKRAIRNPE
> DREARANMHLASAFAGIGFGNAGVHLCHGMSYPISGLVKTYKPKDYNVDHSLVPHGLSVV
> LTSPAVFAFTAQVHPERHLEAAEILGADIRTARIKDAGFILADTLRKFLFDLNVDDGLAA
> IGYSKADIPALVKGTLPQERVTKLSPRPQTEEDLSALFEASMKLY

````


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
````

source .env
JAVA_TOOL_OPTIONS="-Xmx10g" tdb2.tdbquery --loc ../apache-jena-fuseki-5.5.0/run/databases/kendataset --query sparql/neorthines_with_parentage_lite.sparql > data/ontology/ncbi_neornithes_hier.ttl

```
Even this light version didn't stop running after 1h of cpu time.
```

time JAVA_TOOL_OPTIONS="-Xmx10g" tdb2.tdbquery --loc ../apache-jena-fuseki-5.5.0/run/databases/kendataset --query sparql/neorthines_manually_created.sparql > data/ontology/ncbi_neornithes_hier.owl
107.65s user 11.20s system 109% cpu 1:48.79 total

time JAVA_TOOL_OPTIONS="-Xmx8g" tdb2.tdbquery --loc ../apache-jena-fuseki-5.5.0/run/databases/kendataset --query sparql/neorthines_hier.sparql > data/ontology/ncbi_neornithes_timing.owl
JAVA_TOOL_OPTIONS="-Xmx8g" tdb2.tdbquery --loc --query > 6.92s user 0.47s system 280% cpu 2.632 total

```
break
```

Unexpected error making the query: GET https://stars-app.renci.org/ubergraph/sparql?query=SELECT++%2A%0AWHERE%0A++%7B+%7B+?uberon++%3Chttp://purl.obolibrary.org/obo/RO_0002162%3E++%3Chttp://purl.obolibrary.org/obo/NCBITaxon_100%3E+%3B%0A+++++++++++++++%3Chttp://www.w3.org/2000/01/rdf-schema%23label%3E++?uberonLabel%0A++++++OPTIONAL%0A++++++++%7B+%3Chttp://purl.obolibrary.org/obo/NCBITaxon_100%3E%0A++++++++++++++++++++%3Chttp://www.w3.org/2000/01/rdf-schema%23label%3E++?taxonLabel%0A++++++++%7D%0A++++%7D%0A++++FILTER+strstarts%28str%28?uberon%29%2C+%22http://purl.obolibrary.org/obo/UBERON_%22%29%0A++%7D%0A

```

```

# counting relation types

cat data/ontology/sample.uberon.detail.csv | grep "telencephalic song nucleus HVC" | cut -d, -f3 | sort | uniq

````

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
````
