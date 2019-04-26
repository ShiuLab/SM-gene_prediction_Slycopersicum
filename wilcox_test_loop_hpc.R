args = commandArgs(TRUE)
setwd(args[1]) #working directory
nc= args[2] #distance matrix
col_num= integer(args[3]) #number of columns in matrix

nb = paste(c(basename(nc),".wilcoxtest.txt"),collapse='')
## read in table
p1 = read.table(nc, header=T, sep="\t", na.strings = c("", " ","NA"))#,row.names=1)
#subset data- looping through 
nd= "classes_within-btwn_del.txt" #file with within and between pathway classes
p2 = read.table(nd, header=T, sep="\t")
for (j in seq(1, 3, 2)){k=j+1
j=as.numeric(j)
k=as.numeric(k)
nb = paste(c(as.character(p2[j,1]),".wilcoxtest.txt"),collapse='')
d= as.character(p2[j,1])
print(d)
e=as.character(p2[k,1])
p1a <- subset(p1, Class == d | Class == e) 

x <- c(colnames(p1[3:col_num])) #number of columns, not including the class column
cn2 <- col_num-2
d = data.frame(x, pval=rep(0,cn2)) #create empty dataframe based on the number of columns of your original dataframe - 1

##loop to do mann-whitney test on all columns, then append pvalue to dataframe
for (i in 3:col_num) { #change number to total number of columns 
  p1a[,i] <- as.numeric(p1a[,i])
  vname <- p1a[,i]
  df = data.frame(p1a$Class, vname)
  newdf <- na.omit(df)
  y <- wilcox.test(vname ~ p1a.Class, data=newdf, alternative = "two.sided")
  d[i-1,2] <- y$p.value
  }

write.table(d, file = nb, sep="\t")
}