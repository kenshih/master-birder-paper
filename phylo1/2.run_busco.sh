busco -i genomes/chicken_genome/ncbi_dataset/data/GCF_000002315.5/GCF_000002315.5_GRCg6a_genomic.fna -l aves_odb12 -o chicken_busco -m genome --cpu 2 -f
busco -i genomes/hummingbird_genome/ncbi_dataset/data/*/*genomic.fna -l aves_odb12 -o hummingbird_busco -m genome --cpu 1 -f
busco -i genomes/duck_genome/ncbi_dataset/data/*/*genomic.fna -l aves_odb12 -o duck_busco -m genome --cpu 2
#busco -i genomes/alligator_genome/ncbi_dataset/data/*/*genomic.fna -l aves_odb12 -o alligator_busco -m genome --cpu 1x -f
#busco -i turtle_genome/ncbi_dataset/data/*/*genomic.fna -l aves_odb12 -o turtle_busco -m genome --cpu 2
busco -i turtle_genome/ncbi_dataset/data/*/*genomic.fna -l sauropsida_odb12 -o turtle_busco -m genome --cpu 2 -f


