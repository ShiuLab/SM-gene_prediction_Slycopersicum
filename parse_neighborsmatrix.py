#!/usr/bin/python

import sys, os, pandas

def main():
    neighbor_mat = os.path.abspath(sys.argv[1]) #neighbor matrix file      /mnt/home/f0004339/tomato/genomic_clustering/neighbors.txt
    #class_file = os.path.abspath(sys.argv[2]) #SM and GM annotated genes     /mnt/home/f0004339/tomato/clustfiles/Slyc_combinedclass_SMvsPMonly_Tcyc-BM_nodups.txt
    #paralog_file = os.path.abspath(sys.argv[3]) #genes annotated as paralogs    /mnt/home/f0004339/tomato/tomato_paralogs.txt

    class_file = '/mnt/home/f0004339/tomato/clustfiles/Slyc_combinedclass_SMvsPMvsSM-PM_Tcyc-BM.txt'
    paralog_file = '/mnt/home/john3784/3-Solanaceae_project/orthofinder_results/WorkingDirectory/Orthologues_Apr06/New_Analysis_From_Trees_May22/Duplications.csv_paralogs_out.txt'

    df = pandas.read_table(neighbor_mat, sep='\t')
    print(df)
    print(df.columns)
    neighbor_dict = df.drop(['Chromosome'], axis=1).set_index('Gene').T.to_dict('list')
    df.drop(['Chromosome'], axis=1).set_index('Gene').to_csv(open('log.out', 'w+'), sep='\t', header=True, index=True)
    

    # get all genes and their neighbors
    for i in neighbor_dict.keys():
        if isinstance(neighbor_dict[i][0], str):
            neighbor_dict[i] = neighbor_dict[i][0].split(',')
    
    # get all UN, SM, GM, and SM-GM genes
    class_dict = {}
    with open(class_file, 'r') as inf:
        next(inf)
        for line in inf:
            met_class = line.strip().split('\t')[1].replace(' ', '')
            gene = line.strip().split('\t')[0].split('.')[0].replace(' ', '')
            class_dict[gene] = met_class
            
    print(class_dict)
    
    # get all paralogs
    paralog_dict = {}
    with open(paralog_file, 'r') as inf:
        next(inf)
        for line in inf:
            gene1 = line.strip().split('\t')[0].split('.')[0].split('_')
            gene2 = line.strip().split('\t')[1].split('.')[0].split('_')
            gene1 = '_'.join([gene1[2], gene1[3]])
            gene2 = '_'.join([gene2[2], gene2[3]])
            if gene1 not in paralog_dict.keys():
                paralog_dict[gene1] = []
            paralog_dict[gene1].append(gene2)

    # get the neighboring genes
    neighbor_enrich = {}
    no_enrich = []
    for i in neighbor_dict.keys():
        s = []  # SM neighbors
        g = []  # GM neighbors
        sg = [] # SM-GM neighbors
        p = []  # paralog neighbors
        for j in neighbor_dict[i]:
            if j in class_dict.keys():
                if class_dict[j] == 'SM':
                    s.append(j)
                elif class_dict[j] == 'PM':
                    g.append(j)
                elif class_dict[j] == 'SM-PM':
                    sg.append(j)
            if j in paralog_dict.keys():
                p.append(j)

        if len(s) > 0 or len(g) > 0 or len(sg) > 0 or len(p) > 0:
            neighbor_enrich[i] = [s, g, sg, p]
           #print('s %i; g %i; sg %i; p %i' % (len(s), len(g), len(sg), len(p)))
        else:
            no_enrich.append(i)

    # write resulting neighboring genes to file
    # writes 'none' if there are no neighboring genes of that type
    with open('neighbors_matrix.txt', 'w+') as outf:
        outf.write('Gene\tNeighborSM\tNeighborGM\tNeighborSM-GM\tNeighborParalogs\n')
        for i in neighbor_enrich.keys():
            # gene
            outf.write('%s\t' % i)

            # SM clustered genes
            if len(neighbor_enrich[i][0]) > 0:
                outf.write('%s' % ','.join(neighbor_enrich[i][0]))
            else:
                outf.write('none')
            outf.write('\t')
            
            # GM clustered genes
            if len(neighbor_enrich[i][1]) > 0:
                outf.write('%s' % ','.join(neighbor_enrich[i][1]))
            else:
                outf.write('none')
            outf.write('\t')

            # SM-GM clustered genes
            if len(neighbor_enrich[i][2]) > 0:
                outf.write('%s' % ','.join(neighbor_enrich[i][2]))
            else:
                outf.write('none')
            outf.write('\t')
            
            # paralog clustered genes
            if len(neighbor_enrich[i][3]) > 0:
                outf.write('%s' % ','.join(neighbor_enrich[i][3]))
            else:
                outf.write('none')
            outf.write('\n')

        for i in no_enrich:
            outf.write('%s\tnone\tnone\tnone\tnone\n' % i)

    # write resulting counts of genes to file
    # only counts up to 20 neighboring genes of each category
    with open('neighbors_count.txt', 'w+') as outf:
        outf.write('Gene\tNeighborSMCount\tNeighborGMCount\tNeighborSM-GMCount\tNeighborParalogsCount\n')
        for i in neighbor_enrich.keys():
            slen = len(neighbor_enrich[i][0])
            if slen > 20:
                slen = 20
            glen = len(neighbor_enrich[i][1])
            if glen > 20:
                glen = 20
            sglen = len(neighbor_enrich[i][2])
            if sglen > 20:
                sglen = 20
            plen = len(neighbor_enrich[i][3])
            if plen > 20:
                plen = 20
            outf.write('%s\t%i\t%i\t%i\t%i\n' % (i, slen, glen, sglen, plen))
        
        for i in no_enrich:
            outf.write('%s\t0\t0\t0\t0\n' % i)

    # format matrix for kruskal-wallis test
    with open('kruskal-wallis_matrix.txt', 'w+') as outf:
        outf.write('Gene\tClass\tNeighborSMCount\tNeighborGMCount\tNeighborSM-GMCount\n')
        for i in neighbor_enrich:
            if i in class_dict.keys():
                annot_list = [i, class_dict[i]]
                #print(i, neighbor_enrich[i])
            else:
                annot_list = [i, 'UK']
                
            slen = len(neighbor_enrich[i][0])
            if slen > 20:
                slen = 20
            annot_list.append(slen)
                
            glen = len(neighbor_enrich[i][1])
            if glen > 20:
                glen = 20
            annot_list.append(glen)
                
            sglen = len(neighbor_enrich[i][2])
            if sglen > 20:
                sglen = 20
            annot_list.append(sglen)
                                
            annot_count = '\t'.join(str(x) for x in annot_list) + '\n'
            #print(annot_count)
            outf.write(annot_count)
                    

if __name__ == '__main__':
    main()
