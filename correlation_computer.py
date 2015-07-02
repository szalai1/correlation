import math
import json
import sys

############### SEGED FUGGVENYEK ####################################
def sign(x,y):
    if x > y:
        return 1
    elif x < y:
        return -1
    else:
        return 0

def avg(l):
    sum = 0.0
    for i in l:
        sum+= i
    return sum/len(l)

def avg_w(l):
    sum = 0.0
    N = len(l)
    for i in range(N):
        sum +=  (l[i]/(1.0+i))
    return sum

def szum(n):
    ret_val = 0.0
    for i in range(n):
        ret_val += 1.0/(i + 1)
    return ret_val

def min_val(l):
    ret_val = 0;
    first = True
    for i in l:
        num = l[i]
        if first:
            ret_val = num
            first = False
        if ret_val > num:
            ret_val = num
    return ret_val
##############################  szamolok ##############################
""" KENDALL  """
def kendall_tau(list_a, list_b):
    ret_val = 0
    N = len(list_a)
    for i in range(N):
        for j in range(N)[i+1:]:
            sign_a = sign(list_a[i],list_a[j])
            sign_b = sign(list_b[i],list_b[j])
            ret_val += sign_a*sign_b
    return ret_val

def kendall_tau_w(list_a, list_b):
    ret_val = 0
    N = len(list_a)
    for i in range(N):
        for j in range(N)[i+1:]:
            w = ((1.0/(i+1))+(1.0/(j+1)))
            sign_a = sign(list_a[i],list_a[j])
            sign_b = sign(list_b[i],list_b[j])
            ret_val += sign_a*sign_b*w
    return ret_val

def compute_kendall(list_a, list_b):
    print("  [ kendall start ... ]")
    val = kendall_tau(list_a, list_b)
    w_val = kendall_tau_w(list_a, list_b)
    sorted_a = sorted(list_a, reverse=True)
#    list_b = sorted(list_b, reverse=True)
    val_a = kendall_tau(sorted_a, sorted_a)
    val_b = kendall_tau(list_b, list_b)
    w_val_a = kendall_tau_w(sorted_a, sorted_a)
    w_val_b = kendall_tau_w(list_b, list_b )
    print("  [ kendall done ]")
    return [val/math.sqrt(val_a*val_b), w_val/ math.sqrt(w_val_a*w_val_b)]

def kendall(top_list_prev, top_list, sorted_id):
    list_a, list_b = proc_kendall(top_list_prev, top_list, sorted_id)
    return compute_kendall(list_a, list_b)

""" KORRELACIO """

def correl_w(list_a, list_b, s):
    avg_a = avg_w(list_a)/s
    avg_b = avg_w(list_b)/s
    ret_val = 0
    for i in range(len(list_a)):
        w = 1.0/(i+1)
        ret_val += ((list_a[i]- avg_a)*(list_b[i]-avg_b)*w)
    return ret_val

def correl(list_a, list_b, s):
    avg_a = avg(list_a)
    avg_b = avg(list_b)
    ret_val = 0
    for i in range(len(list_a)):
        ret_val += (list_a[i]- avg_a)*(list_b[i]-avg_b)
    return ret_val

def corr(top_list_prev, top_list, sorted_id):
    list_a, list_b = proc_corr(top_list_prev, top_list, sorted_id)
    return compute_corr(list_a, list_b)

def compute_corr(list_a, list_b):
    print("  [ corr start ... ]")
    h_n = szum(len(list_a))
    val = correl(list_a, list_b, h_n)
    w_val = correl_w(list_a, list_b, h_n)
    val_a = correl(list_a, list_a ,h_n)
    val_b = correl(list_b, list_b, h_n)
    w_val_a = correl_w(list_a, list_a, h_n)
    w_val_b = correl_w(list_b, list_b, h_n)
    print("  [ corr done ]")
    return [val/math.sqrt(val_a*val_b), w_val/ math.sqrt(w_val_a*w_val_b)]

################################ FELDOLGOZOK ############################
def write_out(outfile, value_list, time):
    outfile.write(time)
    for i in value_list:
        outfile.write(" "+ str(i))
    outfile.write("\n")

def proc_kendall(l1, l2, sort_id):
    print("kendall lista", l1)
    print( l2)
    print( sort_id)
    print(len(l1), len(l2))
    list_a = []
    list_b = []
    n1 = min_val(l1) - 1
    n2 = min_val(l2) - 1
    for i in sort_id:
        list_b.append(l2[i])
        if i in l1:
            list_a.append(l1[i])
        else:
            list_a.append(n1)
    for i in l1:
        if i not in l2:
            list_b.append(n2)
            list_a.append(l1[i])
    return list_a, list_b

def proc_corr(l1, l2, sort_id):
    print("corr lista", l1)
    print( l2)
    print( sort_id)
    print(len(l1), len(l2))
    list_a = []
    list_b = []
    for i in sort_id:
        list_b.append(l2[i])
        if i in l1:
            list_a.append(l1[i])
        else:
            list_a.append(0.0)
    for i in l1:
        if i not in l2:
            list_b.append(0.0)
            list_a.append(l1[i])
    return list_a, list_b

def pre_proc(day):
    file = open(sys.argv[1]+ "/pagerank_scores_" + str(day) + ".txt_s")
    ret_val = {}
    ret_sort = []
    for line in file:
        splitted = line[:-1].split(" ")
        ret_val[int(splitted[0])] = float(splitted[1])
        ret_sort.append(int(splitted[0]))
    return ret_val, ret_sort

#####################################################################

def compute(top_list_prev, top_list, ret_sort):
    ret_list = []
    ret_list += kendall(top_list_prev, top_list, ret_sort)
    ret_list += corr(top_list_prev, top_list, ret_sort)
    return ret_list
    
def load_json(dirname):
    file_name = dirname + "/intervals.json"
    file = open(file_name)
    return json.load(file)

def main():
    intervals = load_json(sys.argv[1])
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
            centralities  = compute(top_list_prev, top_list, ret_sort)
            centralities.append( inter["interval"]["graph_stat"]["num_nodes"])
            write_out(out_file, centralities, str(inter["interval"]["time"]["start"]) )
        day+=1
        top_list_prev = top_list
        
if __name__ == '__main__':
    main()
