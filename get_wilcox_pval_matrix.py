import sys, os, math, collections
import pandas as pd
import numpy as np
from decimal import Decimal,getcontext

start_dir= sys.argv[1] #directory with .wilcox.test files
oup = open(start_dir + "/sig_path_enriched_continuous_matrix.txt", "w")
df = pd.read_csv(sys.argv[2], sep='\t', index_col = 0)

def clear_space(string): #returns tab-delimited
	string = string.strip()
	while "  " in string:
		string = string.replace("  "," ")
	string = string.replace(" ","_")
	return (string)

def get_median(df): ##use correlation?
    getcontext().prec = 28
    col_list= list(df.columns.values)
    y= len(col_list)
    #df2= df[df.columns[1:y]]
    #print(df2.columns.values)
    newlist= []
    class_list= df['Class'].unique()
    for genetype in class_list:
        genetype1= genetype.split("_")[2]
        genetype2= genetype.split("_")[1]
        genetype3= genetype.split("_")[0]
        if genetype1 == "within":
            pos= genetype
            neg= str(genetype3)+"_"+ str(genetype2) +"_between"
            for i in range(1,len(df.columns)):    
                #get median for each class
                df2 = df.loc[df['Class'] == pos]
                x= df2.columns.values[i]
                print(x)
                x1 = df2.iloc[:,[i]].dropna(axis=0)
                #print(x1[x])
                if x1[x].empty:
                    enrich = 'None'
                    meanpos= 'NA'
                else:
                    meanpos= x1[x].mean()
                    medpos= x1[x].median()
                df3 = df.loc[df['Class'] == neg]
                x2= df3.columns.values[i]
                #print(x2)
                x3 = df3.iloc[:,[i]].dropna(axis=0)
                #print(x3[x2])
                if x3[x2].empty:
                    enrich = 'None'
                    meanneg = 'NA'
                else:    
                    meanneg= x3[x2].mean()
                    medneg= x3[x2].median()
                #print (meanpos, meanneg)
                if meanneg != 'NA' and meanpos != 'NA':
                    print (meanpos, meanneg)
                    if Decimal(meanpos) > Decimal(meanneg):
                        if Decimal(medpos) > Decimal(medneg):
                            enrich = '+'
                        elif Decimal(medpos) == Decimal(medneg):
                            enrich = '+'
                        elif Decimal(medpos) < Decimal(medneg):
                            enrich = '-'
                        else:
                            enrich = 'None'
                            print(medpos, medneg)
                    elif Decimal(meanpos) < Decimal(meanneg):
                        if Decimal(medpos) < Decimal(medneg):
                            enrich = '-'
                        elif Decimal(medpos) == Decimal(medneg):
                            enrich = '-'
                        elif Decimal(medpos) > Decimal(medneg):
                            enrich = '+'
                        else:
                            enrich = 'None'
                            print(medpos, medneg)
                    else:
                        if Decimal(medpos) == Decimal(medneg):
                            enrich = 'None'
                        elif Decimal(medpos) > Decimal(medneg):
                            enrich = '+'
                        elif Decimal(medpos) < Decimal(medneg):
                            enrich = '-'
                        else:
                            enrich = 'None'
                else:
                    enrich = 'None'
                newlist.append([x, pos, meanpos, meanneg, enrich]) 
    
    print(newlist)
    newdf = pd.DataFrame(newlist, columns=['feature','class','pos','neg','enrichment']) #index=['feature']       
    return(newdf)

def get_path_list(dir1, path_list):
    for file in os.listdir(dir1):
        if file.endswith(".wilcoxtest.txt"):
            path= file.strip().split("_")[0]
            path= path.replace("-",".")
            type1= file.strip().split("_")[1]
            if type1== 'SM':
                if path not in path_list:
                    path_list.append(path)
                else:
                    pass
            else:
                pass
    print ("number of pathways: ", len(path_list))
    return path_list

def get_sigs(newfile, dict_score, pathname, feature_list, df2):
    
    #get class enrichment from df2
    #header= newfile.readline()
    pathname= str(pathname)+'_SM_within'
    df3 = df2.loc[df2['class'] == pathname]
    #print(df3)
    for line in newfile:
        x = line.strip().split('\t')
        print(x)
        feat = x[1]
        if x[2]!= 'NA':
            p = float(x[2])
        else:
            p = x[2]
        if feat not in feature_list:
            feature_list.append(feat)
        else:
            pass
        
        df4= df3.loc[df3['feature'] == feat]
        if df4.empty == True:
            if feat not in dict_score:
                    score= float('nan')
                    dict_score[feat] = [score]
            else:
                    dict_score[feat].append(score)
        else:
            df4 = df4.set_index("feature", drop = True)
            #print(df4)
            enrich= df4.loc[feat,'enrichment']
            #print(enrich)
            if p != 'NA':
                if enrich == '+':
                    try:
                        score = float(-(math.log10(p)))
                    except:
                        ValueError
                        score = float(-(math.log10(1e-300)))
                    if feat not in dict_score:
                        dict_score[feat] = [score]
                    else:
                        dict_score[feat].append(score)
                elif enrich == '-':
                    try:
                        score = float(math.log10(p))
                    except:
                        ValueError
                        score = float(math.log10(1e-300))
                    if feat not in dict_score:
                        dict_score[feat] = [score]
                    else:
                        dict_score[feat].append(score)
            else:
                score= float('nan')
                if feat not in dict_score:
                    dict_score[feat] = [score]
                else:
                    dict_score[feat].append(score)
                    
    return(dict_score, feature_list)

                
lista=[]
print("getting SM pathways")
path_list = get_path_list(start_dir, lista)
dict_path= {}
feature_list=[]

print("getting feature enrichment for each pos and neg class")
newdf= get_median(df)
#print(newdf)
for path in path_list:
    for file in os.listdir(start_dir):
        if file.endswith(".wilcoxtest.txt"):
            pathname= file.strip().split("_")[0]
            pathname= pathname.replace("-",".")
            if pathname == path:
                print(path,"getting file features")
                newfile = open(start_dir + "/" + file, 'r') # open file
                header= newfile.readline()
                lines= newfile.readlines()
                print("getting significant features and calculating log pvalue")
                D= {}
                dict_score, feature_list= get_sigs(lines, D, pathname, feature_list, newdf)
                newfile.close()
                dict_path[path]=dict_score
            else:
                pass

print ("dict_path", len(dict_path.keys()))
print ("features", len(feature_list))
feature_str= "\t".join(feature_list)
oup.write("pathway\t%s\n" % (feature_str))

#write output
for path in path_list:
    scoresD= dict_path[path]
    print(scoresD)
    oup.write("%s\t" % (path))
    for feature in feature_list:
        try:
            scores= scoresD[feature]
            oup.write("%.3f\t" % (scores[0]))
        except KeyError:
            scores= 'NA'
            oup.write("%s\t" % (scores))
        
    oup.write("\n")