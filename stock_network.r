#######################
# Author: Te-Yuan Liu
#######################

#######################
# Import Library
#######################
library("igraph")
library(data.table)

#######################
# Define Function
#######################
plot_dd = function(g){
    d = degree(g, mode="all")
    dd = degree.distribution(g, mode="all", cumulative=F)
    degree = 1:max(d)
    probability = dd[-1]
    nonzero.position = which(probability != 0)
    probability = probability[nonzero.position]
    degree = degree[nonzero.position]
    plot(probability ~ degree, xlab="Degree", ylab="Probability", col=1, main="Degree Distribution")
}
#######################
# Main Function
#######################
main = function(){
    dt = fread("stock_network_edgelist.txt", header=F, sep=",", fill=T)
    g = graph.data.frame(dt, directed=F)
    #plot_dd(g)
    g_mst = mst(g)
    plot(g_mst)
}
main()
