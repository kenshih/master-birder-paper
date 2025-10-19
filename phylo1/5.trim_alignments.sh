# in phylo1/
echo "=== Step 3: Trim alignments with TrimAl ==="
mkdir -p alignments/trimmed_alignments

for alignment in alignments/*_aligned.fna; do
    if [ -f "$alignment" ]; then
        gene_name=$(basename "$alignment" _aligned.fna)
        echo "Trimming $gene_name..."
        trimal -in "$alignment" -out "alignments/trimmed_alignments/${gene_name}_trimmed.fna" -automated1
    fi
done
