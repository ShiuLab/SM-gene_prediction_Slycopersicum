'''script parsing path:class:genes files (Slycopersicum_SM-GM_PathIDs-genes_20180606.txt) 
to get gene pairs within pathway A to between pathway A
input: path:class:genes file
'''

import sys, os
import itertools
import random

pathgene_file = open(sys.argv[1], 'r')
output = open(str(sys.argv[1])+'_genepair.txt', 'w')
D={}
lista=[]
def get_path_gene_dict(inp, D, gene_list):
    header= inp.readline()
    for line in inp:
        L= line.strip().split('\t')
        path= L[0]
        class1 = L[1]
        genes = L[2:]
        for gene in genes:
            gene = gene.split('.')[0]
            if gene not in gene_list:
                gene_list.append(gene)
            else:
                pass
        key= str(path)+'_'+str(class1)
        newlist=[]
        if key not in D:
            for gene in genes:
                gene = gene.split('.')[0]
                newlist.append(gene)
            D[key]= newlist
        else:
            print(key, 'already in dict')
    return(D, gene_list)

path_gene_dict, gene_list= get_path_gene_dict(pathgene_file, D, lista)
pathgene_file.close()
print(len(path_gene_dict), 'paths')
print(len(gene_list), "genes")

#get pairs within and between pathways, write output
#output.write('gene_pair\tpath\tclass\tpath_comparison\n')
output.write('gene_pair\tClass\n')
for path in path_gene_dict:
    within=[]
    btwn=[]
    genes= path_gene_dict[path]
    if len(genes) > 0:
         within= itertools.combinations(genes, 2)
         within= list(within)
         for gene in genes:
             for gene2 in gene_list:
                 if gene2 not in genes:
                     btwn.append([gene, gene2])
                 else:
                     pass
         
         print (len(within), path, "within")
         print (len(btwn), path, "between")
         new_btwn_list=[]
         for i in range(1, len(within)+1):
            a = random.choice(btwn)
            new_btwn_list.append(a)
         #path1 = path.split('_')[0]
         #class1 = path.split('_')[1]
         for pair in within:
             pairstr= str(pair[0])+'-'+str(pair[1])
             output.write('%s\t%s_within\n' % (pairstr, path))
         for pair in new_btwn_list:
             pairstr= str(pair[0])+'-'+str(pair[1])
             output.write('%s\t%s_between\n' % (pairstr, path))
         
output.close()
