# SM-gene_prediction_Slycopersicum
This repository will have all scripts and/or links to pipelines used for the SM gene prediction in S. lycopersicum paper

## Obtaining Features

### Domains

1. Map pfam domains to genes using their protein sequence using HMMER. 
    See https://github.com/bmmoore43/Tree_building/ for procedure.

2. Get a binary matrix using parsing script: 

        parse_domain-out_files_getmatrix.py <file with genes:Class> <domain.out file>
        
### Expression

1. Use RNAseq pipeline to process data. See https://github.com/ShiuLab/RNAseq_pipeline for procedure.

2. Use expression matrix to get maximum, median, and variation (MAD):

        get_maxmedMAD_from_exprs.py <dataframe> <directory with expression results file>
