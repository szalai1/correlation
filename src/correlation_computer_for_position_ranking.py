#!/usr/bin/python

import math
import json
import sys
import correlation_computer_for_centrality_ranking as ccfcr

##############################  Calculators ##############################
""" # pytests: test_corr.py passes with Peti's avg_w():
def avg_w(l):
    sum = 0.0
    N = len(l)
    for i in range(N):
        sum +=  (l[i]/(1.0+i))
    return sum
"""

""" KENDALL  """
def compute_kendall(list_a, list_b):
    print("  [ kendall start ... ]")
    val = ccfcr.kendall_tau(list_a, list_b)
    w_val = ccfcr.kendall_tau_w(list_a, list_b)
    sorted_a = sorted(list_a, reverse=False) # due to position ranking ascending order is needed
#    list_b = sorted(list_b, reverse=False)
    val_a = ccfcr.kendall_tau(sorted_a, sorted_a)
    val_b = ccfcr.kendall_tau(list_b, list_b)
    w_val_a = ccfcr.kendall_tau_w(sorted_a, sorted_a)
    w_val_b = ccfcr.kendall_tau_w(list_b, list_b )
    print("  [ kendall done ]")
    return [val/math.sqrt(val_a*val_b), w_val/ math.sqrt(w_val_a*w_val_b)]

def kendall(top_list_prev, top_list, sorted_id):
    list_a, list_b = proc_kendall(top_list_prev, top_list, sorted_id)
    return compute_kendall(list_a, list_b)

""" KORRELACIO """
def correl(list_a, list_b, s):
    n = len(list_a)
    avg_normal = float(n+1) / 2
    
    avg_weighted_a = ccfcr.avg_w(list_a)/s
    avg_weighted_b = ccfcr.avg_w(list_b)/s
    """
    avg_weighted_a = avg_w(list_a)/s
    avg_weighted_b = avg_w(list_b)/s
    """
    ret_val = 0.0
    ret_val_w = 0.0
    for i in range(n):
        w = 1.0/(i+1)
        #print list_a[i], list_b[i], avg_normal
        ret_val += (list_a[i] - avg_normal)*(list_b[i] - avg_normal)
        ret_val_w += ((list_a[i]- avg_weighted_a) * (list_b[i]-avg_weighted_b) * w)
    return ret_val, ret_val_w

def correl_var(n, s):
    avg = float(n+1) / 2
    
    avg_weighted = ccfcr.avg_w(range(1,n+1))/s
    """
    avg_weighted = avg_w(range(1,n+1))/s
    """
    ret_val = 0.0
    ret_val_w = 0.0
    for i in range(n):
        w = 1.0/(i+1)
        ret_val += math.pow(i+1 - avg,2)
        ret_val_w += (math.pow(i+1 - avg_weighted,2) * w)
    return ret_val, ret_val_w

def compute_corr(list_a, list_b):
    print("  [ corr start ... ]")
    n = len(list_a)
    h_n = ccfcr.szum(n)
    val, w_val = correl(list_a, list_b, h_n)
    var, w_var = correl_var(n, h_n)
    print("  [ corr done ]")
    return [val / var, w_val / w_var]

def corr(top_list_prev, top_list, sorted_id):
    """ 
    print top_list_prev
    print top_list
    print sorted_id
    """
    list_a, list_b = proc_corr(top_list_prev, top_list, sorted_id)
    #print list_a
    #print
    #print list_b
    return compute_corr(list_a, list_b)

################################ Processors ############################

def proc_kendall(l1, l2, sort_id):
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

def proc_corr(l1, l2, sort_id):
    print("kendall lista")
    list_a = []
    list_b = []
    n1 = len(l1) + 1.0 # number of vertices in last interval + 1
    n2 = len(l2) + 1.0 # number of vertices in current interval + 1
    sum_a = 0.0
    sum_b = 0.0
    counter_a = 0
    counter_b = 0
    for i in sort_id:
        if not i in l1:
            counter_a += 1
            sum_a += n1
            n1 += 1
    for i in l1:
        if i not in l2:
            counter_b += 1
            sum_b += n2
            n2 += 1

    if counter_a > 0:
        avg_a = sum_a / counter_a
    else:
        avg_a = 0.0

    if counter_b > 0:
        avg_b = sum_b / counter_b
    else: 
        avg_b = 0.0

    for i in sort_id:
        list_b.append(l2[i])
        if i in l1:
            list_a.append(l1[i])
        else:
            list_a.append(avg_a) # tie on last position
    for i in l1:
        if i not in l2:
            list_b.append(avg_b) # tie on last position
            list_a.append(l1[i])
    return list_a, list_b

def pre_proc(centrality_data_folder, input_file_prefix, day):
    ret_val, ret_sort = ccfcr.pre_proc(centrality_data_folder, input_file_prefix, day)
    return  centrality_to_position(ret_val, ret_sort)

def centrality_to_position(ret_val, ret_sort):
    ret_pos_val = {}
    summed_rank = 0.0
    i = 0
    j = 1
    N = len(ret_sort)
    for j in range(1,N+1):
        summed_rank += j
        if j == N or ret_val[ret_sort[j-1]] > ret_val[ret_sort[j]]:
            for k in range(i,j):
                ret_pos_val[ret_sort[k]] = summed_rank / (j-i)
            i = j
            summed_rank = 0.0
    return ret_pos_val, ret_sort

#####################################################################

def compute(top_list_prev, top_list, ret_sort, correls):
    ret_list = []
    if "kendall" in correls:
        ret_list += kendall(top_list_prev, top_list, ret_sort)
    if "corr" in correls:
        ret_list += corr(top_list_prev, top_list, ret_sort)
    return ret_list

def main():
    centrality_data_folder = sys.argv[1]
    input_file_prefix = sys.argv[2]
    output_file = sys.argv[3]
    metric = sys.argv[4]
    intervals = ccfcr.load_json(centrality_data_folder)
    out_file = open(output_file, 'w')
    day = 0
    top_list_prev = []
    top_list = []
    ret_sort = []
    num_nodes = 1
    for inter in intervals["centrality_test"]["intervals"]:
        print("[ day = " + str(day) +" ]")
        if  inter["interval"]["graph_stat"]["num_nodes"] != 0:
            top_list, ret_sort = pre_proc(centrality_data_folder, input_file_prefix, day)
            num_prev_nodes = num_nodes
            num_nodes = inter["interval"]["graph_stat"]["num_nodes"]
        else:
            #out_file.write(str(inter["interval"]["time"]["start"])+" - - 0 -1.0 -1.0\n")
            out_file.write(str(day)+" - - 0 -1.0 -1.0\n")
            day+=1
            continue
        if day != 0:
            #centralities = [str(inter["interval"]["time"]["start"])]
            centralities = [str(day)]
            centralities += compute(top_list_prev, top_list, ret_sort, metric)
            num_new_nodes = inter["interval"]["graph_stat"]["new_nodes"]
            num_deleted_nodes = inter["interval"]["graph_stat"]["deleted_nodes"]
            centralities.append(num_nodes)
            centralities.append(float(num_new_nodes) / num_nodes)
            centralities.append(float(num_deleted_nodes) / num_prev_nodes)
            ccfcr.write_out(out_file, centralities)
        day+=1
        top_list_prev = top_list
        
if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 5:
        main()
    else:
        print 'Usage: <centrality_data_folder> <input_file_prefix> <output_file> <kendall/corr>'
