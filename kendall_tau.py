import math
import json
import sys

def sign(x,y):
    if x > y:
        return 1
    elif x < y:
        return -1
    else:
        return 0

def kendall_tau_w(list_a, list_b, s):
    ret_val = 0
    N = len(list_a)
    for i in range(N):
        for j in range(N)[i+1:]:
            w = ((1.0/(i+1))+(1.0/(j+1)))
            sign_a = sign(list_a[i],list_a[j])
            sign_b = sign(list_b[i],list_b[j])
            ret_val += sign_a*sign_b*w
    return ret_val

def kendall_tau(list_a, list_b, s):
    ret_val = 0
    N = len(list_a)
    for i in range(N):
        for j in range(N)[i+1:]:
            sign_a = sign(list_a[i],list_a[j])
            sign_b = sign(list_b[i],list_b[j])
            ret_val += sign_a*sign_b
    return ret_val

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

def corr_w(list_a, list_b, s):
    avg_a = avg_w(list_a)/s
    avg_b = avg_w(list_b)/s
    ret_val = 0
    for i in range(len(list_a)):
        w = 1.0/(i+1)
        ret_val += ((list_a[i]- avg_a)*(list_b[i]-avg_b)*w)
    return ret_val

def corr(list_a, list_b, s):
    avg_a = avg(list_a)
    avg_b = avg(list_b)
    ret_val = 0
    for i in range(len(list_a)):
        ret_val += (list_a[i]- avg_a)*(list_b[i]-avg_b)
    return ret_val

def pre_proc(score_list, n ):
    ret_val = {}
    ii = 0
    ret_sort = []
    for i in score_list:
        ii+=1
        if ii > n:
            break
        ret_val[i["id"]] =float(i["value"])
        ret_sort.append(i["id"])
    return ret_val, ret_sort

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

def proc(l1, l2, sort_id):
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
            sort_id.append(i)
            list_b.append(n2)
            list_a.append(l1[i])
    return list_a, list_b, sort_id

def proc2(l1, l2, sort_id):
    list_a = []
    list_b = []
    n1 = 0.0
    n2 = 0.0
    for i in sort_id:
        list_b.append(l2[i])
        if i in l1:
            list_a.append(l1[i])
        else:
            list_a.append(n1)
    for i in l1:
        if i not in l2:
            sort_id.append(i)
            list_b.append(n2)
            list_a.append(l1[i])
    return list_a, list_b, sort_id

def szum(n):
    ret_val = 0.0
    for i in range(n):
        ret_val += 1.0/(i + 1)
    return ret_val

def sorted2(l,reverse):
    return l 

def main():
    f = open(sys.argv[1])
    data = json.load(f)
    first = True
    prev = {}
    results = []
    prev_sort = []
    if sys.argv[3] == "w_corr":
        func = corr_w
        pr = proc2
        sor = sorted2
    elif sys.argv[3] == "corr":
        func = corr
        pr = proc2
        sor = sorted2
    elif sys.argv[3]  == "kendall":
        func = kendall_tau
        pr = proc
        sor = sorted
    elif sys.argv[3] == "w_kendall":
        func = kendall_tau_w
        pr = proc
        sor = sorted
    else:
        return
        
    for inter in data["centrality_test"]["intervals"]:
        act_k = int(inter["interval"]["graph_stat"]["num_nodes"])
        if sys.argv[2] not in inter["interval"]["measures"]:
            print(str(inter["interval"]["time"]["start"])+" -" )
            continue
        act, act_sort = pre_proc(inter["interval"]["measures"][sys.argv[2]], act_k)
        if first:
            prev = act
            prev_k = act_k
            first = False
            continue

        a, b, s = pr(prev, act, act_sort)
        h_n = szum(len(s))
        val  = func(a,b,h_n)
        sorted_b = sor(b,reverse=True)
        sorted_a = sor(a, reverse=True)
        s_1 = func(sorted_b,sorted_b,h_n)
        s_2 = func(sorted_a,sorted_a,h_n)
        prev = act
        prev_sort = act_sort
        print(str(inter["interval"]["time"]["start"])+" "+ str(val/math.sqrt(s_1*s_2)))
    
if __name__ == '__main__':
    main()
