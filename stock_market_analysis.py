#######################
# Author: Te-Yuan Liu
#######################

#######################
# Import Library
#######################
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
#######################
# Define Function
#######################
def preprocess(weekly):
    print("start preprocessing...")
    get_id = False
    p_dic = {}
    q_dic = {}
    r_dic = {}
    edgelist_dic = {}
    file_count = 0
    valid_count = 0
    path = "./finance_data/data/"
    idx_list = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            file_count += 1
            file_name = str(file).strip(".csv")
            df = pd.read_csv(path + str(file), header=0)
            d_list = df["Date"].tolist()
            p_list = df["Close"].tolist()
            if len(p_list) == 765:
                valid_count += 1                
                if weekly and not get_id:
                    get_id = True
                    for i in range(len(d_list)):
                        objs = d_list[i].split("-")
                        if len(objs) != 3:
                            print(objs)
                            print("date obj length error...")
                            return
                        mydate = datetime.date(int(objs[0]), int(objs[1]), int(objs[2]))
                        if mydate.strftime("%A") == "Monday":
                            idx_list.append(i)
                if weekly:
                    p_list = [p_list[i] for i in idx_list]
                p_dic[file_name] = p_list
    for s, pl in p_dic.items():
        q_list = []
        r_list = []
        for i in range(1,len(pl)):
            q = (pl[i] - pl[i-1])/pl[i-1]
            q_list.append(q)
            r_list.append(np.log(1 + q))
        q_dic[s] = q_list
        r_dic[s] = r_list
    for s1, rl1 in r_dic.items():
        for s2, rl2 in r_dic.items():
            if s1 != s2:
                key1 = s1 + "\n" + s2
                key2 = s2 + "\n" + s1
                if edgelist_dic.get(key1) == None and edgelist_dic.get(key2) == None:
                    ri_avg = sum(rl1)/len(rl1)
                    rj_avg = sum(rl2)/len(rl2)
                    product_list = [a*b for a,b in zip(rl1,rl2)]
                    ri_rj_avg = sum(product_list)/len(product_list)
                    ri_sq_list = [a**2 for a in rl1]
                    ri_sq_avg = sum(ri_sq_list)/len(ri_sq_list)
                    rj_sq_list = [a**2 for a in rl2]
                    rj_sq_avg = sum(rj_sq_list)/len(rj_sq_list)
                    pij = (ri_rj_avg - ri_avg*rj_avg)/np.sqrt((ri_sq_avg - ri_avg**2)*(rj_sq_avg - rj_avg**2))
                    if pij > 1 or pij < -1:
                        print("pij value error...")
                        return
                    wij = np.sqrt(2*(1 - pij))
                    edgelist_dic[key1] = wij
                elif edgelist_dic.get(key1) != None and edgelist_dic.get(key2) != None:
                    print("duplicate entry error...")
                    return
    ## create edge list file
    outfile_name = "stock_network_edgelist.txt"
    if weekly:
        outfile_name = "weekly_stock_network_edgelist.txt"
    with open(outfile_name, "w") as outfile:
        for k, v in edgelist_dic.items():
            s1, s2 = k.split("\n")
            line = ",".join([s1, s2, str(v)]) + "\n"
            outfile.write(line)
   
    print("preprocessing completed...")
    return edgelist_dic

def plot_hist(dic):
    ## plot histogram
    w_list = []
    for k, v in edgelist_dic.items():
        w_list.append(v)
    plt.hist(w_list, bins="auto")
    plt.title("Histogram")
    plt.xlabel("Edge weight")
    plt.ylabel("Count")
    plt.show()
   
def paint():
    path = "./finance_data/"
    df = pd.read_csv(path + "Name_sector.csv", header=0)
    n_list = df["Symbol"].tolist()
    s_list = df["Sector"].tolist()
    if len(n_list) != len(s_list):
        print("list length equality error...")
        return
    s_n_dic = {}
    c_list = []
    for i in range(len(n_list)):
        s = s_list[i]
        n = n_list[i]
        if s_n_dic.get(s) == None:
            tmp_list = []
            tmp_list.append(n)
            s_n_dic[s] = tmp_list
        else:
            s_n_dic[s].append(n)    
    print(len(s_n_dic))
    n_s_dic = {}
    s_count = 0
    for s, nl in s_n_dic.items():
        for n in nl:
            n_s_dic[n] = s_count
        s_count += 1
    print(s_count)
    with open("stock_color_mapping.txt", "w") as outfile:
        for k, v in n_s_dic.items():
            line = ",".join([k, str(v)]) + "\n"
            outfile.write(line)
def metric():
    path = "./finance_data/data/"
    name_dic = {}
    for file in os.listdir(path):
        if file.endswith(".csv"):
            file_name = str(file).strip(".csv")
            df = pd.read_csv(path + str(file), header=0)
            p_list = df["Close"].tolist()
            if len(p_list) == 765:
                name_dic[file_name] = 1
    path = "./finance_data/"
    df = pd.read_csv(path + "Name_sector.csv", header=0)
    n_list = df["Symbol"].tolist()
    s_list = df["Sector"].tolist()
    if len(n_list) != len(s_list):
        print("list length equality error...")
        return
    s_n_dic = {}
    for i in range(len(n_list)):
        s = s_list[i]
        n = n_list[i]
        if s_n_dic.get(s) == None:
            tmp_list = []
            tmp_list.append(n)
            s_n_dic[s] = tmp_list
        else:
            s_n_dic[s].append(n)    
    alpha = 0.0
    trim_s_n_dic = {}
    for s, nl in s_n_dic.items():
        tmp_list = []
        for n in nl:
            if name_dic.get(n) != None:
                tmp_list.append(n)
        trim_s_n_dic[s] = tmp_list
    for s, nl in trim_s_n_dic.items():
        for n in nl:
            alpha += len(nl)
    alpha = alpha/(len(name_dic)**2)
    print(alpha)

#######################
# Main Function
#######################
def main():
    preprocess(True)
    #paint()
    #metric()
if __name__ == "__main__":
    main()
