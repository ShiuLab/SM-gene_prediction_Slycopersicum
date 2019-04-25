### parse orthofinder, get orthologues for each gene

import sys, os, pandas
from itertools import combinations


inp= open(sys.argv[1], 'r')
species1= str(sys.argv[2]) ## first column species abbreviation or NA
species2= str(sys.argv[3]) ## second column species abbreviation or NA
output= open(sys.argv[1]+'.orthopairs.txt', 'w')

def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 

header= inp.readline()
par_dict1={}
par_dict2={}
for line in inp:
    new_list= []
    new_list2=[]
    L=line.strip().split('\t')
    ortho= L[0]
    orig= L[1].split(",")
    homolog= L[2].split(",")
    for gene in orig:
        if species1 == 'NA':
            new_list.append(gene)
        else:
            gene= gene.split(species1)[1]
            new_list.append(gene)
    for gene2 in homolog:
        if species2 == 'NA':
            new_list2.append(gene2)
        else:
            gene2= gene2.split(species2)[1]
            new_list2.append(gene2)
    
    #final= new_list + new_list2
    if ortho not in par_dict1:
            par_dict1[ortho]=new_list
    else:
            for i in new_list:
                par_dict1[ortho].append(i)
    if ortho not in par_dict2:
            par_dict2[ortho]=new_list2
    else:
            for i in new_list2:
                par_dict2[ortho].append(i)

print (par_dict1, par_dict2)

output.write("gene\tortholog\n")
for og in par_dict1:
    data_list= par_dict1[og]
    data_list= Remove(data_list)
    data_list2= par_dict2[og]
    data_list2= Remove(data_list2)
    #print (data_list, len(data_list))
    #for combo in combinations(data_list, 2):
    for x in data_list:
        for y in data_list2:
            genelist= [x, y]
            tup_str= '\t'.join(genelist)
            output.write('%s\n' % tup_str)

inp.close()
output.close()
        