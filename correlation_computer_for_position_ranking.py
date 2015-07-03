import math
import json
import sys
import correlation_computer_for_centrality_ranking as ccfcr

##############################  szamolok ##############################
""" KENDALL  """

def compute_kendall(list_a, list_b):
    print("  [ kendall start ... ]")
    val = ccfcr.kendall_tau(list_a, list_b)
    w_val = ccfcr.kendall_tau_w(list_a, list_b)
    sorted_a = sorted(list_a, reverse=False) # itt a poziciok miatt novekvo sorrendben kell rendezni
#    list_b = sorted(list_b, reverse=False)
    val_a = ccfcr.kendall_tau(sorted_a, sorted_a)
    val_b = ccfcr.kendall_tau(list_b, list_b)
    w_val_a = ccfcr.kendall_tau_w(sorted_a, sorted_a)
    w_val_b = ccfcr.kendall_tau_w(list_b, list_b )
    print("  [ kendall done ]")
    return [val/math.sqrt(val_a*val_b), w_val/ math.sqrt(w_val_a*w_val_b)]

def kendall(top_list_prev, top_list, sorted_id):
    list_a, list_b = proc_vertices(top_list_prev, top_list, sorted_id)
    return compute_kendall(list_a, list_b)

""" KORRELACIO """

def corr(top_list_prev, top_list, sorted_id):
    list_a, list_b = proc_vertices(top_list_prev, top_list, sorted_id)
    return ccfcr.compute_corr(list_a, list_b)

################################ FELDOLGOZOK ############################

def proc_vertices(l1, l2, sort_id):
    print("kendall lista")
    list_a = []
    list_b = []
    n1 = len(l1) # number of vertices in last interval
    n2 = len(l2) # number of vertices in current interval
    for i in sort_id:
        list_b.append(l2[i])
        if i in l1:
            list_a.append(l1[i])
        else:
            list_a.append(n1+1) # tie on last position
    for i in l1:
        if i not in l2:
            list_b.append(n2+1) # tie on last position
            list_a.append(l1[i])
    return list_a, list_b

def pre_proc(day):
    file = open(sys.argv[1]+ "/pagerank_scores_" + str(day) + ".txt_s")
    ret_val = {}
    ret_sort = []
    rank = 1.0
    for line in file:
        splitted = line[:-1].split(" ")
        ret_val[int(splitted[0])] = rank
        ret_sort.append(int(splitted[0])) #ezt el lehetne hagyni. De inkabb taroljuk a csucsok id-jat is. 
        rank += 1
    return ret_val, ret_sort    

#####################################################################

def main():
    intervals = ccfcr.load_json(sys.argv[1])
    out_file = open(sys.argv[2], 'w')
    day = 0
    top_list_prev = []
    top_list = []
    ret_sort = []
    for inter in intervals["centrality_test"]["intervals"]:
        print("[ day = " + str(day) +" ]")
        if  inter["interval"]["graph_stat"]["num_nodes"] != 0:
            top_list, ret_sort = pre_proc(day)
        else:
            out_file.write(str(inter["interval"]["time"]["start"])+" -\n")
            continue
        if day != 0:
            centralities = [str(inter["interval"]["time"]["start"])]
            centralities += ccfcr.compute(top_list_prev, top_list, ret_sort, sys.argv[3:])
            centralities.append( inter["interval"]["graph_stat"]["num_nodes"])
            centralities.append(inter["interval"]["graph_stat"]["new_nodes"])
            ccfcr.write_out(out_file, centralities)
        day+=1
        top_list_prev = top_list
        
if __name__ == '__main__':
    main()
