##script used to combine multiple contrast files into a matrix
#python sum_contrasts.py <start directory> <output file name> <file with all genes you want)
import os, sys

start_dir = sys.argv[1]
class_file = open(sys.argv[2], 'r')
ec_file= open(sys.argv[3], 'r')
sum_matrix = open(sys.argv[4],"w")
#get all emzyme genes
all_gene_list=[]
for line in ec_file:
    g= line.strip().split('\t')[0]
    if g not in all_gene_list:
        all_gene_list.append(g)
    else:
        print(g, "duplicate gene")
#function that adds file data to a dictionary
def add_data_to_dict(inp, D, all_gene_list):
    gene_list=[]
    for line in inp:
        if line.startswith("gene"):
            pass
        else:
            L = line.strip().split("\t")
            #print L
            if len(L) > 2:
                gene = L[0]
                if gene not in gene_list:
                    gene_list.append(gene)
                    PM = L[1]
                    PM2 = L[2]
                    SM = L[3]
                    SM2= L[4]
                    SMPM= L[5]
                    SMPM2= L[6]
                    if gene not in D:
                        D[gene] = [PM, PM2, SM, SM2, SMPM, SMPM2]
                    else:
                        D[gene].append(PM)
                        D[gene].append(PM2)
                        D[gene].append(SM)
                        D[gene].append(SM2)
                        D[gene].append(SMPM)
                        D[gene].append(SMPM2)
                else:
                    print (gene, "dup")
                
            else:
                gene = L[0]
                print(gene, "no data")
        
    for gene in all_gene_list:
        if gene in gene_list:
            pass
        else:
            if gene not in D:
                D[gene] = ['NA', 'NA', 'NA', 'NA', 'NA', 'NA']
            else:
                D[gene].extend(['NA', 'NA', 'NA', 'NA', 'NA', 'NA'])


Dclass = {}
#get classes
for line in class_file:
    L= line.strip().split('\t')
    gene = L[0]
    class1 = L[1]
    if gene not in Dclass:
        Dclass[gene] = class1
    else:
        print (gene, "duplicated")
#loop through directory for each file to add input and each filename
title_list = []
dir2 = start_dir + "/"
D = {}
for file in os.listdir(dir2):
    if file.endswith("med-max.txt"):
        namelist = file.strip().split('.txt')
        name= namelist[0]
        print (name)
        nameGM = name+"_GM-med"
        nameGM2 = name+"_GM-max"
        nameSM = name+"_SM-med"
        nameSM2 = name+"_SM-max"
        nameSMGM = name+"SM_GM-med"
        nameSMGM2 = name+"SM_GM-max"
        title_list.append(nameGM)
        title_list.append(nameGM2)
        title_list.append(nameSM)
        title_list.append(nameSM2)
        title_list.append(nameSMGM)
        title_list.append(nameSMGM2)
        inp = open(dir2 + "/" + file)
        add_data_to_dict(inp, D, all_gene_list)
        inp.close()
title_str = "\t".join(title_list)
print (D)
print (title_list)
#write heading for gene and each filename
sum_matrix.write("gene\tClass\t%s\n" % title_str)

#write corr data to each gene
for gene in D.keys():
        data_list= D[gene]
        try:
            class1 = Dclass[gene]
        except KeyError:
            class1 = "unkn"
        string= "\t".join(data_list)
        sum_matrix.write(gene + "\t%s\t%s\n" % (class1, string))
sum_matrix.close()
