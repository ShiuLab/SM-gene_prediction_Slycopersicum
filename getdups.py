#!/user/bin/python

import sys


def checkdups(nodesdict, sly_genes1, sly_genes2, spnode):
    for node in (node for node in nodesdict.keys() if node < spnode):
        for key in (key for key in nodesdict[node].keys() if nodesdict[node][key]):
            for gene in sly_genes1:
                if gene in nodesdict[node][key]:
                    nodesdict[node][key].remove(gene)
            for gene in nodesdict[node][key]:
                if gene in nodesdict[node][key]:
                    nodesdict[node][key].remove(gene)


def getslygenes(genes, sp):
    slygenes = []
    for gene in genes:
        if sp in gene:
            slygenes.append(gene)
    return slygenes



if __name__ == '__main__':
    nodesdict = {}

    sp= str(sys.argv[2])
    with open(sys.argv[1], 'r') as inf:
        #next(inf)
        for line in inf:
            l = line.strip().split('\t')
            #ogroup = l[0]      # orthogroup
            spnode = l[1]       # species tree node
            #genenode = l[2]    # gene tree node
            #supp = l[3]        # bootstrap value
            type = l[4]         # terminal (paralogs) or shared (orthologs and paralogs)
            genes1 = l[5].strip().split(', ')
            genes2 = l[6].strip().split(', ')

            #print(type)
            if type == "Shared":    # non-terminal node
                if spnode.startswith("N"):
                    spnode = int(spnode.replace("N",""))

                sly_genes1 = getslygenes(genes1, sp)
                sly_genes2 = getslygenes(genes2, sp)

                if not sly_genes1 and not sly_genes2:
                    pass
                else:
                    if spnode not in nodesdict.keys():
                        nodesdict[spnode] = {"genes1": sly_genes1, "genes2": sly_genes2}
                    else:
                        nodesdict[spnode]["genes1"].extend(sly_genes1)
                        nodesdict[spnode]["genes2"].extend(sly_genes2)

                #checkdups(nodesdict, sly_genes1, sly_genes2, spnode)
    nodelist = sorted(nodesdict.keys())

    with open(sp+ "_dups_GENES1.txt", "w+") as outf1:
        with open(sp+ "_dups_GENES2.txt", "w+") as outf2:
            for i in nodelist:
                for key in nodesdict[i]:
                    if key == "genes1":
                        for item in nodesdict[i][key]:
                            outf1.write("%s\t%s\n" % (i,item))
                    elif key == "genes2":
                        for item in nodesdict[i][key]:
                            outf2.write("%s\t%s\n" % (i,item))
