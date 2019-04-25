# SM-gene_prediction_Slycopersicum
This repository will have all scripts and/or links to pipelines used for the SM gene prediction in S. lycopersicum paper

## Obtaining Features

### Domains

1. Map pfam domains to genes using their protein sequence using HMMER. 
    See https://github.com/bmmoore43/Tree_building/ for procedure.

2. Get a binary matrix using parsing script: 

        python parse_domain-out_files_getmatrix.py <file with genes:Class> <domain.out file>
        
### Expression

1. Use RNAseq pipeline to process data. See https://github.com/ShiuLab/RNAseq_pipeline for procedure.

2. Use expression matrix to get maximum, median, and variation (MAD):

        python get_maxmedMAD_from_exprs.py <dataframe> <directory with expression results file>
        
3. Get matrix of differenetially expressed genes. Note: may need to change label of files to loop through and index where FC and p-value are:

        python sum_contrasts_updwnNC2_loop.py <directory containing output FC files> <output matrix name>
        
4. Get expression (FC) breadth for significant matrix:

        python get_expr_breadth.py <significant FC matrix file>
        
5. For all "_expr_breadth.txt"  files, summarize into a matrix:

        python sum_contrasts_exprbreadth.py <directory where "_expr_breadth.txt" files are>
