##script used to combine multiple contrast files into a matrix
#python sum_contrasts.py <start directory> <output file name>
import os, sys

start_dir = sys.argv[1]
#file = open(sys.argv[1])
sum_matrix = open(sys.argv[2],"w")

#function that adds file data to a dictionary
def add_data_to_dict(inp,D,Dclass):
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
                    class1 = L[1]
                    up = L[2]
                    dwn = L[3]
                    if gene not in Dclass:
                        Dclass[gene] = class1
                    else:
                        pass
                    if gene not in D:
                        D[gene] = [up,dwn]
                    else:
                        D[gene].append(up)
                        D[gene].append(dwn)
                else:
                    print (gene, "dup")
                
            else:
                gene = L[0]
                if gene not in gene_list:
                    gene_list.append(gene)
                    class1 = L[1]
                    up = "NA"
                    dwn = "NA"
                    if gene not in Dclass:
                        Dclass[gene] = class1
                    else:
                        pass
                    if gene not in D:
                        D[gene] = [up,dwn]
                    else:
                        D[gene].append(up)
                        D[gene].append(dwn)
                else:
                    print (gene, "dup")

D = {}
Dclass = {}
#loop through directory for each file to add input and each filename
title_list = []
dir2 = start_dir + "/"
for file in os.listdir(dir2):
    if file.endswith("_expr_breadth.txt"):
        name = file.strip().split('_expr_breadth.txt')[0]
        nameup = name+"_up"
        namedwn = name+"_dwn"
        title_list.append(nameup)
        title_list.append(namedwn)
        inp = open(dir2 + "/" + file)
        add_data_to_dict(inp, D, Dclass)
        inp.close()
title_str = "\t".join(title_list)
print (D)
print (title_list)
#write heading for gene and each filename
sum_matrix.write("gene\tClass\t%s\n" % title_str)

#write logFC data to each gene
for gene in D:
    data_list= D[gene]
    class1 = Dclass[gene]
    #for data in data_list:
    string= "\t".join(data_list)
    sum_matrix.write(gene + "\t%s\t%s\n" % (class1, string))
sum_matrix.close()
#file.close()