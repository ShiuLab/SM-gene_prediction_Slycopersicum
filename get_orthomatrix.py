import sys
import os
import numpy as np
import pandas as pd

all_genes_list=[]
start_dir = sys.argv[1] #directory with orthologue groups from orthofinder
all_genes_file= open(sys.argv[2], "r") #file with all genes
prefix= str(sys.argv[3]) #species prefix applied from Orthofinder

for line in all_genes_file: #get all genes
    if line.startswith("gene"):
        pass
    else:
        L = line.strip().split('\t')
        gene= L[0]
        if gene not in all_genes_list:
            all_genes_list.append(gene)

#df = pd.read_csv(all_genes_file, sep='\t', header=0)
#print (df)

def get_orthologs(inp, all_genes_list, D):

    col_list= []
    header= inp.readline()
    for line in inp:
        L= line.strip().split("\t")
        genes = L[1].split(",")
        for gene in genes:
            gene= gene.split(".")[0] #get rid of alt splice
            #print(gene)
            gene= gene.split(prefix)[1] #get rid of prefix
            col_list.append(gene)
    
    for i in all_genes_list:
        if i in col_list:
            if i not in D:
                D[i]= [1] #need to make first item a list in order to append
            else:
                D[i].append(1)
        else:
            if i not in D:
                D[i] = [0]
            else:
                D[i].append(0)
            
gene_dict= {}
title_list= ["gene"]
for file in os.listdir(start_dir):
    if file.endswith(".csv"):
        name = file.strip()
        print (name)
        title_list.append(name)
        inp = open(start_dir + "/" + file, "r")
        get_orthologs(inp, all_genes_list, gene_dict)
        inp.close()

print (gene_dict)
print (title_list)
title_str = "\t".join(title_list)
output= open("ortholog_matrix.txt", "w")
output.write('%s\n' % (title_str))
for gene in gene_dict:
    data_list= gene_dict[gene]
    datastr= '\t'.join(str(x) for x in data_list)
    if gene.startswith(prefix):
        gene= gene.split(prefix)[1]
        output.write("%s\t%s\n" % (gene, datastr))
    else:
        #print (gene)
        output.write("%s\t%s\n" % (gene, datastr))

output.close()

#df.to_csv("ortholog_matrix.txt", sep="\t", header=True)
        