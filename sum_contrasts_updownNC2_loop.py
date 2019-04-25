'''script used to combine multiple contrast files into a matrix and determines whether a gene is significantly
up or down regulated by a FC >= 1 for up and FC <= -1 for down and an adj_pvalue <= 0.05
USAGE: python sum_contrasts_updownNC2_loop.py [directory containing contrast files] [output matrix name]
'''
import os, sys

start_dir = sys.argv[1]
#file = open(sys.argv[1])
sum_matrix = open(sys.argv[2],"w")

def add_data_to_dict(inp,D):
    header=inp.readline()
    for line in inp:
        L = line.strip().split("\t")
        if len(L) > 1:
            gene = L[0]
            FC = L[1]
            adj_pvalue = L[5]
            if float(adj_pvalue) <=0.05:
                if float(FC) >= 1:
                    if gene not in D:
                        D[gene] = ["up"]
                    else:
                        D[gene].append("up")
                else:
                    if float(FC) <= -1:
                        if gene not in D:
                            D[gene] = ["down"]
                        else:
                            D[gene].append("down")
                    else:
                        if gene not in D:
                            D[gene] = ["NC"]
                        else:
                            D[gene].append("NC")
            else:
                if gene not in D:
                    D[gene] = ["NC"]
                else:
                    D[gene].append("NC")

D = {}
#add_data_to_dict(file, D)
#loop through directory for each file to add input and each filename
title_list = []
for file in os.listdir(start_dir):
    if file.startswith("contrast_"):
        name = file.strip().split("_")
        print (name)
        title_list.append(name[1])
        inp = open(start_dir + "/" + file)
        add_data_to_dict(inp,D)
        inp.close()
title_str = "\t".join(title_list)
print (title_str)
print (D)
#write heading for gene and each filename
sum_matrix.write("gene\t %s\n" % title_str)

#write logFC data to each gene
for gene in D:
    data_list= D[gene]
    #for data in data_list:
    string= "\t".join(data_list)
    sum_matrix.write(gene + "\t" + "%s" % string + "\n")
sum_matrix.close()
#file.close()