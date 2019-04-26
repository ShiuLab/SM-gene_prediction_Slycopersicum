#!/user/bin/python

import sys


def makedict(inf):
    dict = {}

    for line in inf:
        l = line.strip().split('\t')
        spnode = int(l[0])
        gene = l[1].split('.')[0]
        gene = gene.split("Slycopersicum_Sly_")[1]

        if spnode not in dict.keys():
            dict[spnode] = []
        else:
            dict[spnode].append(gene)

    return dict


def dedupe(genes):
    return set(genes)


def remove_all(list, gene):
    for i in (i for i in list if i == gene):
        list.remove(i)
    return list


def parse(dict):
    keys = list(dict.keys())

    a = len(keys) - 1
    b = a - 1

    while a > 0:
        while b >= 0:
            print(keys[a], keys[b])
            for gene in dict[keys[a]]:
                if gene in dict[keys[b]]:
                    #dict[keys[b]] = list(dict[keys[b]])
                    dict[keys[b]] = remove_all(dict[keys[b]], gene)
            b -= 1
        a -= 1
        b = a - 1

    return dict


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as genes1:
        g1 = makedict(genes1)

    with open(sys.argv[2], 'r') as genes2:
        g2 = makedict(genes2)

    combined = {}
    for key in g1.keys():
        combined[key] = g1[key] + g2[key]
        #print(len(combined[key]))
        combined[key] = dedupe(combined[key])
        #print(combined[key])
        #print(len(combined[key]))

    for key in combined.keys():
        combined[key] = list(combined[key])

    mostrec = parse(combined)

    with open("parsed_mostrecentdups_combined.txt", "w+") as outf:
        outf.write("node\tgene\n")
        for key in mostrec.keys():
            for gene in mostrec[key]:
                outf.write("%s\t%s\n" % (key, gene))
