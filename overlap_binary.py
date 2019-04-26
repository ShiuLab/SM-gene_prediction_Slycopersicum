import os,sys
import pandas as pd
import numpy as np
import random
import scipy
from scipy import stats
import math

'''
	input1: binary matrix
	input2: Class of positive and negative gene pairs
	
'''

inp = open(sys.argv[2],'r').readlines()[1:]
file = sys.argv[1]
out = open(sys.argv[1]+'_genepair_overlap.txt','w')


# out.write(open(sys.argv[2],'r').readlines()[0].strip() + '\tOverlap_%s_larger_0\tOverlap_%s_larger_1\tOverlap_%s_larger_5\tOverlap_%s_larger_10\n'%(sys.argv[3],sys.argv[3],sys.argv[3],sys.argv[3]))
# if 'Fold_changes' in type or 'FC' in type:
# 	out.write(open(sys.argv[2],'r').readlines()[0].strip() + '\tOverlap_%s_larger_0\tOverlap_%s_smaller_0\tOverlap_%s_larger_1\tOverlap_%s_smaller_1\tOverlap_%s_larger_2\tOverlap_%s_smaller_2\n'%(sys.argv[3],sys.argv[3],sys.argv[3],sys.argv[3],sys.argv[3],sys.argv[3]))

df = pd.read_csv(file, sep='\t', index_col = 0, header = 0)  ### the first column as index, which equals rownames in R, the first row as header
#get title
title = 'Gene_pair\tClass'
for sam in df.columns[1:]:
    title += '\t'+ sam
title += '\n'
out.write(title)

#get values of matrix and calculate distance
#rowname = df.index.tolist()
rowname = df.index.values
for i in range(0, len(rowname)):
    rowname[i]= rowname[i].split('.')[0] #change gene number to get rid of alt splice
x = 0
while x < len(inp):
	inl = inp[x]
	gene1 = inl.split('\t')[0].split('-')[0]
	gene2 = inl.split('\t')[0].split('-')[1]
	if gene1 in rowname and gene2 in rowname:
		res = inl.strip()
		for sam in df.columns[1:]:
			value1 = df.loc[gene1,sam]
			value2 = df.loc[gene2,sam]
			if value1 == 1 and value2 == 1:
				final_val= 1
			else:
				final_val= 0
			res += '\t%s'%final_val
		out.write(res + '\n')
	x += 1

out.close()