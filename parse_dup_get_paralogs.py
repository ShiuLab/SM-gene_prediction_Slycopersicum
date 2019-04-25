# get paralogs

import sys
import pandas as pd
from itertools import combinations

def clear_spaces(string): #returns tab-delimited
	string = string.strip()
	while "  " in string:
		string = string.replace("  "," ")
	string = string.replace(" ","_")
	return string

df = open(sys.argv[1], 'r')
output = open(str(sys.argv[1])+'_paralogs_out.txt', "w")
header=  df.readline()
par_dict={}
for line in df:
    L= line.strip().split('\t')
    
    ortho= L[0]
    sp_node= L[1]
    gn_node= L[2]
    tm= L[4]
    gene_list= L[5:]
    #print(ortho, sp_node, gn_node, tm)
    if sp_node == 'Slycopersicum':
        if ortho not in par_dict:
            par_dict[ortho]=[]
            for i in gene_list:
                if ',' in i:
                    ilist= i.split(',')
                    for i in ilist:
                        i = clear_spaces(i)
                        par_dict[ortho].append(i)
                else:
                    i = clear_spaces(i)
                    par_dict[ortho].append(i) 
        else:
            for i in gene_list:
                if ',' in i:
                    ilist= i.split(',')
                    for i in ilist:
                        i = clear_spaces(i)
                        par_dict[ortho].append(i)
                else:
                    i = clear_spaces(i)
                    par_dict[ortho].append(i)

#print(par_dict)
output.write('gene\tparalog\n')
for og in par_dict:
    data_list= par_dict[og]
    print (data_list, len(data_list))
    for combo in combinations(data_list, 2):
    #result= list(itertools.combinations(, 2))
        gen1=list(combo)[0]
        gen2=list(combo)[1]
        genelist= [gen1, gen2]
        #print(gen1, gen2)
        tup_str= '\t'.join(genelist)
        output.write('%s\n' % tup_str)

df.close()
output.close()