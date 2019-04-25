import sys, os
import pandas as pd
import numpy as np
import statsmodels
from statsmodels import robust


def main():

    for i in range (1,len(sys.argv),2):
            if sys.argv[i] == "-df":
                DF1 = sys.argv[i+1]
            if sys.argv[i] == "-start_dir":
                start_dir = sys.argv[i+1]
            

    df1 = pd.read_csv(DF1, sep='\t', index_col = 0)
    #df2 = pd.DataFrame(index= list(df.index))
    
    def get_max_stat(inp):
        #for each row in inp
        resultmax = max(inp)
        #resultmed = np.median(inp)
        return resultmax
    def get_med(inp):
        resultmed = np.median(inp)
        return resultmed

    for file in os.listdir(start_dir):
        if file.startswith("Results_"):
            name= file.strip().split("for_")[1]
            df2 = pd.read_csv(file, sep='\t', index_col = 0)
            print (file)
            #df2= pd.DataFrame(data=robust.scale.mad(df, axis=1), columns=['MAD'], index= list(df.index))
            df3 = pd.DataFrame(index= list(df2.index))
            df3[str(name)+'_MAD']= robust.scale.mad(df2, axis=1)
            df3[str(name)+'_max']= df2.apply(get_max_stat, axis=1)
            df3[str(name)+'_median']= df2.apply(get_med, axis=1)
            df1= pd.concat([df1, df3], axis=1, join='inner')
    
    print (df1)
    df1.to_csv(path_or_buf=str(DF1)+".MAD_max_med.txt", sep="\t", index=True, header=True)
        
if __name__ == '__main__':
	main()