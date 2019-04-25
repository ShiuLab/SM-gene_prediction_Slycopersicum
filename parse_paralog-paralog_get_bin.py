## parse paralog-paralog file, get binary

import os, sys

paralogfile = open(sys.argv[1], 'r') #paralog file where paralogs are paired: gene1 \t paralog-gene1
all_genes_file = open(sys.argv[2], "r") #file with all genes, and their class
sum_matrix= open(sys.argv[1]+ "bin_matrix.txt", "w") #output

paralog_list= []
for line in paralogfile:
        if line.startswith('gene'):
            pass
        else:
            L= line.strip().split('\t')
            #gene= L[0].split("_")[4]
            gene= L[0].split(".")[0]
            #paralog= L[1].split("_")[4]
            paralog= L[1].split(".")[0]
            paralog_list.append(gene)
            paralog_list.append(paralog)

print("paralogs", paralog_list, len(paralog_list))
Dclass= {}            
for line in all_genes_file:
        if line.startswith('gene'):
            pass
        else:
            L= line.strip().split('\t')
            gene= L[0]
            class1= L[1]
            if gene not in Dclass:
                Dclass[gene]= class1
            else:
                print (gene, class1, 'gene duplicated')
                

sum_matrix.write("gene\tclass\tparalog\n")
#write output
for gene in Dclass:
    class1 = Dclass[gene]
    if gene in paralog_list:
        para = 1
    else:
        para = 0
    
    sum_matrix.write('%s\t%s\t%s\n' % (gene, class1, para))

