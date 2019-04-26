import sys,os
import pandas as pd
import numpy as np
import random
import scipy
from scipy.stats.stats import pearsonr
from scipy import stats
#from scipy.stats import chisqprob
import math
'''
	input1: FC or FPKM matrix
	input2: Class of positive and negative gene pairs
	
'''

inp = open(sys.argv[2],'r').readlines()[1:]
file = sys.argv[1]
out = open(str(sys.argv[1])+'genepair_distance.matrix.txt','w')
df = pd.read_csv(file, sep='\t', index_col = 0, header = 0)  ### the first column as index, which equals rownames in R, the first row as header
#get title
title = 'Gene_pair\tClass'
for sam in df.columns[2:]:
    title += '\tDistance_' + sam
title += '\n'
out.write(title)
#get values of matrix and calculate distance
rowname = df.index.tolist()
x = 0
while x <= len(inp):
	inl = inp[x]
	#print(inl)
	if inl.startswith("gene"):
	    pass
	else:
	   gene1 = inl.split('\t')[0].split('-')[0]
	   gene2 = inl.split('\t')[0].split('-')[1]
	   if gene1 in rowname and gene2 in rowname:
	       res = inl.strip()
	       for sam in df.columns[2:]:
	           value1 = df.loc[gene1,sam]
	           value2 = df.loc[gene2,sam]
	           #print (value1, value2)
	           if value1 != 0 or value2 != 0:
	               distance = abs(value1-value2)/((value1**2 + value2**2)**0.5)
	               if distance != 1 and distance != 0:
	                   distance = distance.round(3)
	               else:
	                   distance = 0
	               res += '\t%s'%distance
	       out.write(res + '\n')
	x += 1

out.close()
	