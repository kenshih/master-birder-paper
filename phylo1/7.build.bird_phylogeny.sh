
echo "=== Step 5: Build phylogenetic tree with IQ-TREE ==="
echo "Running IQ-TREE with model selection and bootstrap support..."

iqtree -s concatenated_alignment.fna -m MFP -bb 1000 -nt AUTO --prefix bird_phylogeny/bird_phylogeny

echo "=== ANALYSIS COMPLETE! ==="
echo "Results:"
echo "- Phylogenetic tree: bird_phylogeny.treefile"
echo "- Bootstrap tree: bird_phylogeny.contree"
echo "- Log file: bird_phylogeny.log"

echo "View your tree online: Upload to iTOL (https://itol.embl.de/)"

ls -lh bird_phylogeny.*
