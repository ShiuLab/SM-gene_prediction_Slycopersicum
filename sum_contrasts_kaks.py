##script used to combine multiple contrast files into a matrix
#python sum_contrasts.py <start directory>  <class file> <output file name>
#python ~/Github/parse_scripts/sum_contrasts_kaks.py /mnt/home/john3784/3-Solanaceae_project/ML_matrices/Athal_model \
#Aracyc_SMvsGMvsSMGM_20180723.txt Athaliana_kaks_allspec_matrix_190308.txt
import os, sys
import numpy as np
start_dir = sys.argv[1]
class_file = open(sys.argv[2])
sum_matrix = open(sys.argv[3],"w")

#function that adds file data to a dictionary
def add_data_to_dict(inp,D2,all_gene_list):
    D={}
    head= inp.readline()
    for line in inp:
        L = line.strip().split("\t")
        gene = L[0].split('.')[0]
        ka = L[2]
        ks = L[3]
        if ka != "-" and ks != "-":
            if float(ks) == 0:
                kaks = float(ka)/float(0.0000001)
            else:
                kaks = float(ka)/float(ks)
            if gene not in D:
                D[gene] = [kaks]
            else:
                D[gene].append(kaks)
        else:
            pass
                
    for gene in all_gene_list:
        if gene in D:
            kaks_list= D[gene]
            maxkaks= max(kaks_list)
            medkaks= np.median(kaks_list)
            if gene not in D2:
                D2[gene]= [maxkaks, medkaks]
            else:
                D2[gene].append(maxkaks)
                D2[gene].append(medkaks)
        else:
            maxkaks= "NA"
            medkaks= "NA"
            if gene not in D2:
                D2[gene]= [maxkaks, medkaks]
            else:
                D2[gene].append(maxkaks)
                D2[gene].append(medkaks)

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
all_gene_list= Dclass.keys()
#loop through directory for each file to add input and each filename
title_list = []
dir2 = start_dir + "/"
D2 = {}
for file in os.listdir(dir2):
    if file.endswith("_generate.txt"):
        print (file)
        name = file.strip().split('_fin')[0]
        print (name)
        namemax = name+"_maxKaKs"
        namemed = name+"_medKaKs"
        title_list.append(namemax)
        title_list.append(namemed)
        inp = open(dir2 + "/" + file)
        add_data_to_dict(inp, D2, all_gene_list)
        inp.close()
title_str = "\t".join(title_list)
print (D2)
print (title_list)
#write heading for gene and each filename
sum_matrix.write("gene\tClass\t%s\n" % title_str)

#write logFC data to each gene
for gene in D2:
    data_list= D2[gene]
    try:
        class1 = Dclass[gene]
    except KeyError:
        print ("gene not in class dict", gene)
        class1 = "unkn"
    
    data_list2= []
    for data in data_list:
        data2= str(data)
        data_list2.append(data2)
    string= "\t".join(data_list2)
    sum_matrix.write(gene + "\t%s\t%s\n" % (class1, string))
sum_matrix.close()
#file.close()