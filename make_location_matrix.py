#!/usr/bin/python

import sys, os, pandas

def find_neighbors(chr, df):
    neighbor_dict = {}

    smalldf = df.loc[df['Chromosome']==chr]

    for gene1 in smalldf.index:
        if smalldf.at[gene1,'Chromosome'] != chr:
            if not neighbor_dict.keys():
                continue
            else:
                break
        else:
            gene_start = smalldf.at[gene1,'Start']
            gene_end = smalldf.at[gene1,'End']
            gene_start_bound = gene_start - 100000
            gene_end_bound = gene_end - 100000

            #print(gene_start_bound, gene_end_bound)

            for gene2 in smalldf.index:
                if gene2 == gene1:
                    continue
                else:
                    if smalldf.at[gene2,'Start'] > gene_start_bound or smalldf.at[gene2,'End'] < gene_end_bound:
                        if gene1 not in neighbor_dict.keys():
                            neighbor_dict[gene1] = []
                        genenum = int(gene1.split("_")[1])
                        upbnd= genenum+10
                        lowbnd= genenum-10
                        genenum2= int(gene2.split("_")[1])
                        if (genenum2 <= upbnd) and (genenum2 >= lowbnd):
                            neighbor_dict[gene1].append(gene2)
        #print(neighbor_dict[gene1])

    return neighbor_dict


def main():
    gff_file = os.path.abspath(sys.argv[1])
    #SMGM_file = os.path.abspath(sys.argv[2])
    #paralog_file = os.path.abspath(sys.argv[3])

    annot_dict = {}
    chr_dict = {}
    with open(gff_file, 'r') as inf:
        tempS, tempE = 0, 0
        for line in inf:
            if line.startswith('#'):
                pass
            else:
                l = line.strip().split()
                if l[2] == 'gene':
                    tempS = int(l[3])
                    tempE = int(l[4])

                    while 'CDS' not in line:
                        line = next(inf)
                        #print(line)
                        if '###' in line:
                            break

                    if 'Genbank:' in line:
                        geneID = line.split('Genbank:')[1].split('.')[0]
                        chromosome = line.split('\t')[0].split('.')[0]
                        if geneID not in annot_dict.keys():
                            annot_dict[geneID] = []
                        annot_dict[geneID] = [chromosome, tempS, tempE]

                        if chromosome not in chr_dict.keys():
                            chr_dict[chromosome] = []
                        chr_dict[chromosome].append(geneID)

    df = pandas.DataFrame(data=annot_dict).T.rename(columns={0:'Chromosome',1:'Start',2:'End'})
    df = df.sort_values(by=['Chromosome', 'Start'])
    df.index.name = 'Gene'

    with open('location_matrix.txt', 'w+') as outf:
        df.to_csv(path_or_buf=outf, sep='\t')

    neighbor_dict = {}
    for i in chr_dict.keys():
        print(i)
        neighbor_dict[i] = find_neighbors(i, df)

    with open('neighbors.txt', 'w+') as outf:
        outf.write("Chromosome\tGene\tNeighbors(up/down 10kbp)\n")

        for i in neighbor_dict.keys(): #chromosome
            for j in neighbor_dict[i]:
                kgenes = []
                for k in neighbor_dict[i][j]:
                    kgenes.append(k)
                outf.write('%s\t%s\t%s\n' % (i, j, ','.join(kgenes)))

    #neighbors_df = pandas.read_table('neighbors_matrix.txt', sep='\t')
    #print(neighbors_df)



if __name__ == '__main__':
    main()
