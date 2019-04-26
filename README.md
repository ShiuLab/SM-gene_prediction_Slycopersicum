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

### Co-expression

#### Expression correlation

1. Scripts to create correlation matrix can be found here: https://github.com/ShiuLab/Gene_coexpression_scripts/tree/master/Similariry_measures

2. After getting the correlation matrix of the expression set, the median and maximum of each type of correlation for each gene to each SM, GM, and DA class was taken by:

        python get_med-max_corr_from_corr-file.py <correlation matrix> <gene:class file>
        
#### Expression clustering

1. R scripts were used to obtain kmeans, cmeans, hierarchical clustering, and wgcna clustering and are available here: https://github.com/ShiuLab/Gene_coexpression_scripts/tree/master/Clustering.

2. In order to combine all cluster files into a categorical matrix:

        python get_cluster_lists_as_matrix.py <directory where cluster files are> <file with all genes you want to use>
        
3. Now turn the categorical matrix into a binary one to use in machine learning. Script to convert to binary can be found here: https://github.com/ShiuLab/ML-Pipeline/blob/master/

        python get_cat_as_bin2.py <categorical matrix>


### Evolutionary data

#### Orthologs

1. Use Orthofinder to get orthologs and paralogs: https://github.com/ShiuLab/OrthoFinder

2. Genes were considered to be homologous if they were in the same orthogroup. Parse out orthologous genes to binary format:
    
        python get_orthomatrix.py <directory with all ortholog files> <file with all genes from your species>
    
3. Get paralogs (within species homologs) pairs using Duplications.csv file from Orthofinder:

        python parse_dup_get_paralogs.py Duplications.csv species_name
        
4. Remove duplicate pairs:

        python remove_dup_rows_pd.py <file>

5. parse paralog data to get binary:

        python parse_paralog-paralog_get_bin.py <paralog pair file>

6. get orthologous pairs:

        python parse_orthofinder_orthologue_file_getpairs.py <ortho _file> <species1> <species2>
        
#### Ka/Ks

1. To determine Ka/Ks, inputs needed include species protein sequence and gene coding sequence, as well as paired gene list.

2. To run on hpc, old python version is needed. Clustal and Paml also need to be installed. If running on hpc, paml and clustal can be found at the directories in the command line.

        module purge
        module load icc/2015.1.133-GCC-4.9.2
        module load imp/5.0.2.044
        module load Python/2.7.9
        
3. Run rate pair script. The control file <yn00.ctl> should be in the same directory that you run the script in.

        python AlnUtility.py -f rate_pair -pep <peptide sequence> -cds <coding sequence> -p paml -paml /mnt/home/peipeiw/Documents/Solanales/cds/test/paml/paml4.9a/bin/yn00 -clustal /mnt/home/peipeiw/Documents/Solanales/cds/test/ClustalX1.83/clustalw-2.1-linux-x86_64-libcppstatic -pairs <pair list>
        
 4. Summarize Ka/Ks values in matrix. This script takes the median and maximum ka/ks values for each gene.
 
        python sum_contrasts_kaks.py <start dir> <class file> <output>

### Duplication data

#### Genomic clustering

1. Make a location and neighbors matrix, ie. for each gene the genes within 100kb and 10 genes.

        python make_location_matrix.py <gff_file>
        
2. Using neighbors matrix, parse genes which are SM, GM, DA, and paralogs

        python parse_neighborsmatrix.py <neighbors_matrix> <class_file> <paralog_file>
        
#### Most recent duplication node

1. Get node for each gene:

        python getdups.py <Duplications.csv> <species you want>
        
2. Get most recent duplication node:

        parse_mostrecentdups_combined.py <genes1> <genefile2> <species abbreviation>

        

