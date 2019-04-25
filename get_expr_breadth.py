#calculate expression breadth from significant logFC matrix
import sys

inp = open(sys.argv[1], "r") #significant logFC matrix
output = open(sys.argv[1]+"_expr_breadth.txt", "w")

D1={}

for line in inp:
    if line.startswith("AT"):
        L = line.strip().split("\t")
        gene = L[0]
        data_list= L[1:]
        i = 0
        j = 0
        k = 0
        for x in data_list:
            if x == "up":
                i = i+1
                k = k+1
            elif x == "down":
                j = j+1
                k = k+1
            else:
                pass
        if gene not in D1:
            D1[gene] = [str(i),str(j),str(k)]
        else:
            print (gene, "duplicate")
            
print(D1)

output.write("gene\texpr_breadth_uponly\texpr_breadth_downonly\texpr_breadth_up.down\n")
for gene in D1:
    data = D1[gene]
    datastr = "\t".join(data)
    output.write("%s\t%s\n" % (gene, datastr))
    