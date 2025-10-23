busco -i genomes/chicken_genome/ncbi_dataset/data/GCF_000002315.5/GCF_000002315.5_GRCg6a_genomic.fna -l sauropsida_odb12 -o busco_out/chicken -m genome --cpu 3 -f
busco -i genomes/hummingbird_genome/ncbi_dataset/data/*/*genomic.fna -l sauropsida_odb12 -o busco_out/hummingbird -m genome --cpu 4 -f
busco -i genomes/duck_genome/ncbi_dataset/data/*/*genomic.fna -l sauropsida_odb12 -o busco_out/duck -m genome --cpu 4 -f
busco -i genomes/lizard_genome/ncbi_dataset/data/*/*genomic.fna -l sauropsida_odb12 -o busco_out/lizard -m genome --cpu 1 -f


