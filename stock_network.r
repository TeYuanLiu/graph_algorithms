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
color_dic = function(filepath){
    con = file(filepath, "r")
    lin = readLines(con)
    n_v = NULL
    s_v = NULL
    for(i in 1:length(lin)){
        objs = strsplit(lin[i], ",")[[1]]
        n_v = c(n_v, objs[1])
        s_v = c(s_v, as.numeric(objs[2]))
    }
    names(s_v) = n_v
    close(con)
    s_v
}
color_assign = function(g, dic){
    for(i in 1:vcount(g)){
        V(g)[i]$color = dic[V(g)[i]$name] + 1
    }
    g
}
metric = function(g){
    alpha = 0.0
    for(i in 1:vcount(g)){
        v_s = V(g)[i]$color
        n_v = neighbors(g, V(g)[i], mode="all")
        for(j in 1:length(n_v)){
            if(v_s == n_v[j]$color){
                alpha = alpha + 1/length(n_v)
            }
        }
    }
    alpha = alpha/vcount(g)
    print(alpha)
}
#######################
# Main Function
#######################
main = function(){
    edgelist_filepath = "weekly_stock_network_edgelist.txt"
    dt = fread(edgelist_filepath, header=F, sep=",", fill=T)
    n_s_filepath = "stock_color_mapping.txt"
    g = graph.data.frame(dt, directed=F)
    E(g)$weight = E(g)$V3
    vsize = rep(4, vcount(g))
    vlabelsize = rep(0.2, vcount(g))
    #plot_dd(g)
    n_s_dic = color_dic(n_s_filepath)
    g_color = color_assign(g, n_s_dic)
    g_mst = mst(g_color)
    metric(g_mst)
    plot(g_mst, vertex.color=V(g_mst)$color, vertex.size=vsize, vertex.label.cex=vlabelsize)
}
main()
