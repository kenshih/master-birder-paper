Here's a summary of what we did to get BUSCO working from your local installation:

## BUSCO Installation Summary

### Problem
- BUSCO was failing with "No module named 'Bio'" error
- Missing Python dependencies for the local BUSCO installation

### Solution Steps

1. **Activated the mamba environment properly**
   ```bash
   source sourceme  # This runs: eval "$(mamba shell hook --shell zsh)" and mamba activate phylo
   ```

2. **Installed missing Python dependencies**
   ```bash
   # Install Biopython (provides 'Bio' module)
   mamba install -c conda-forge biopython
   
   # Install data analysis packages
   mamba install -c conda-forge pandas numpy matplotlib seaborn
   
   # Install HTTP requests library
   mamba install -c conda-forge requests
   ```

3. **Installed BUSCO from local directory**
   ```bash
   pip install -e ../../busco
   ```

4. **Verified installation**
   ```bash
   busco -h  # Should show BUSCO 6.0.0 help message
   ```

### Key Dependencies Installed
- `biopython` - For the 'Bio' module
- `pandas` - For data manipulation
- `numpy` - For numerical operations
- `matplotlib` & `seaborn` - For plotting
- `requests` - For HTTP functionality

### Final Result
- BUSCO 6.0.0 successfully installed and functional
- All dependencies resolved
- Ready to run BUSCO analyses

### Additional Note: BBTools Issue
If you encounter the error "bbtools tool cannot be found", you can skip BBTools (which is only used for assembly statistics) by adding the `--skip_bbtools` flag to your BUSCO command:

```bash
busco -i your_sequence.fasta -l lineage_dataset -o output_name -m genome --skip_bbtools
```

The key was ensuring the mamba environment was properly activated before installing dependencies, and then installing BUSCO in development mode (`-e` flag) from the local directory.

```
$cd /Users/ken/Documents/wk/master-birder-paper/phylo1 && wget https://sourceforge.net/projects/bbmap/files/latest/download -O bbmap.tar.gz

$ cd /Users/ken/Documents/wk/master-birder-paper/phylo1 && export PATH=$PWD/bbmap:$PATH && which bbmap.sh
/Users/ken/Documents/wk/master-birder-paper/phylo1/bbmap/bbmap.sh
$ cd /Users/ken/Documents/wk/master-birder-paper/phylo1 && export PATH=$PWD/bbmap:$PATH && busco -i genomes/lizard_genome/ncbi_dataset/data/*/*genomic.fna -l sauropsida_odb12 -o busco_out/lizard -m genome --cpu 1 -f
2025-10-21 20:31:38 INFO:       ***** Start a BUSCO v6.0.0 analysis, current time: 10/21/2025 20:31:38 *****
2025-10-21 20:31:38 INFO:       Configuring BUSCO with local environment
2025-10-21 20:31:38 INFO:       Running genome mode
2025-10-21 20:31:38 INFO:       'Force' option selected; overwriting previous results directory
2025-10-21 20:31:38 INFO:       Downloading information on latest versions of BUSCO data...
2025-10-21 20:31:41 INFO:       Input file is /Users/ken/Documents/wk/master-birder-paper/phylo1/genomes/lizard_genome/ncbi_dataset/data/GCF_963506605.1/GCF_963506605.1_rZooViv1.1_genomic.fna
2025-10-21 20:31:41 INFO:       The local file or folder /Users/ken/Documents/wk/master-birder-paper/phylo1/busco_downloads/lineages/sauropsida_odb12 is the last available version.
2025-10-21 20:31:45 INFO:       Running BUSCO using lineage dataset sauropsida_odb12 (eukaryota, 2025-07-01)
2025-10-21 20:31:45 INFO:       Running 1 job(s) on bbtools, starting at 10/21/2025 20:31:45
2025-10-21 20:31:50 INFO:       [bbtools]       1 of 1 task(s) completed
2025-10-21 20:31:50 INFO:       Running 1 job(s) on miniprot_index, starting at 10/21/2025 20:31:50
2025-10-21 20:33:02 INFO:       [miniprot_index] 1 of 1 task(s) completed
2025-10-21 20:33:06 INFO:       Running 1 job(s) on miniprot_align, starting at 10/21/2025 20:33:06
2025-10-22 01:59:42 INFO:       [miniprot_align] 1 of 1 task(s) completed
2025-10-22 01:59:50 INFO:       ***** Run HMMER on gene sequences *****
2025-10-22 02:00:02 INFO:       Running 6109 job(s) on hmmsearch, starting at 10/22/2025 02:00:02
2025-10-22 02:00:40 INFO:       [hmmsearch]     611 of 6109 task(s) completed
2025-10-22 02:01:03 INFO:       [hmmsearch]     1222 of 6109 task(s) completed
2025-10-22 02:01:25 INFO:       [hmmsearch]     1833 of 6109 task(s) completed
2025-10-22 02:01:51 INFO:       [hmmsearch]     2444 of 6109 task(s) completed
2025-10-22 02:02:18 INFO:       [hmmsearch]     3055 of 6109 task(s) completed
2025-10-22 02:02:41 INFO:       [hmmsearch]     3666 of 6109 task(s) completed
2025-10-22 02:03:04 INFO:       [hmmsearch]     4277 of 6109 task(s) completed
2025-10-22 02:03:29 INFO:       [hmmsearch]     4888 of 6109 task(s) completed
2025-10-22 02:03:52 INFO:       [hmmsearch]     5499 of 6109 task(s) completed
2025-10-22 02:04:17 INFO:       [hmmsearch]     6109 of 6109 task(s) completed
2025-10-22 02:04:20 INFO:       210 candidate overlapping regions found
2025-10-22 02:04:20 INFO:       59219 exons in total
2025-10-22 02:04:35 WARNING:    550 of 5982 Complete matches (9.2%) contain internal stop codons in Miniprot gene predictions
2025-10-22 02:04:37 INFO:

    -------------------------------------------------------------------------------------------
    |Results from dataset sauropsida_odb12                                                     |
    -------------------------------------------------------------------------------------------
    |C:97.8%[S:95.4%,D:2.4%],F:0.2%,M:2.1%,n:6118,E:9.2%                                       |
    |5982    Complete BUSCOs (C)    (of which 550 contain internal stop codons)                |
    |5837    Complete and single-copy BUSCOs (S)                                               |
    |145    Complete and duplicated BUSCOs (D)                                                 |
    |10    Fragmented BUSCOs (F)                                                               |
    |126    Missing BUSCOs (M)                                                                 |
    |6118    Total BUSCO groups searched                                                       |
    -------------------------------------------------------------------------------------------
2025-10-22 02:04:37 INFO:       BUSCO analysis done with WARNING(s). Total running time: 19976 seconds

***** Summary of warnings: *****
2025-10-22 02:04:35 WARNING:busco.busco_tools.hmmer       550 of 5982 Complete matches (9.2%) contain internal stop codons in Miniprot gene predictions

2025-10-22 02:04:37 INFO:       Results written in busco_out/lizard
2025-10-22 02:04:37 INFO:       For assistance with interpreting the results, please consult the userguide: https://busco.ezlab.org/busco_userguide.html

2025-10-22 02:04:37 INFO:       Visit this page https://gitlab.com/ezlab/busco#how-to-cite-busco to see how to cite BUSCO
2025-10-22 02:04:40 INFO:       Thank you for using BUSCO! Anonymous usage data is gathered to improve the tool. You may opt out with --opt-out-run-stats.
```