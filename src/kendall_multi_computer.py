import math, json, sys, os
import correlation_computer_for_centrality_ranking as ccfcr

##############################  szamolok ##############################
""" KENDALL  """
# here we can use the same embedded loop for both value computation
def kendall_tau_all(list_a, list_b, list_a_sorted): 
    ret_val = 0
    ret_val_w = 0
    ret_val_a = 0
    ret_val_a_w = 0
    ret_val_b = 0
    ret_val_b_w = 0
    N = len(list_a)
    for i in range(N):
        for j in range(N)[i+1:]:
            #print i,j
            w = ((1.0/(i+1))+(1.0/(j+1)))
            sign_a = ccfcr.sign(list_a[i],list_a[j])
            sign_a_sorted = ccfcr.sign(list_a_sorted[i],list_a_sorted[j])
            sign_b = ccfcr.sign(list_b[i],list_b[j])
            ret_val += sign_a*sign_b # normal
            ret_val_w += sign_a*sign_b*w # weighted
            ret_val_a += sign_a_sorted*sign_a_sorted # normal for list_a_sorted
            ret_val_a_w += sign_a_sorted*sign_a_sorted*w # weighted for list_a_sorted
            ret_val_b += sign_b*sign_b # normal for list_b
            ret_val_b_w += sign_b*sign_b*w # weighted for list_b
    return ret_val, ret_val_w, ret_val_a, ret_val_a_w, ret_val_b, ret_val_b_w

def kendall_all(list_a, list_b): # both lists are preprocessed by kendal_multi_preproc.py
    print("  [ kendall start ... ]")
    sorted_a = sorted(list_a, reverse=True)
#    list_b = sorted(list_b, reverse=True)
    val, w_val, val_a, w_val_a, val_b, w_val_b = kendall_tau_all(list_a, list_b, sorted_a)
    print("  [ kendall done ]")
    return [val/math.sqrt(val_a*val_b), w_val/ math.sqrt(w_val_a*w_val_b)]

################################ FELDOLGOZOK ############################
def load_toplist(toplist_file_name):
    f = open(toplist_file_name)
    toplist = []
    for line in f:
        splitted = line[:-1].split(" ")
        toplist.append(float(splitted[0]))
    f.close()
    return toplist

#####################################################################

def main():
    preproc_folder = sys.argv[1]
    interval_id = int(sys.argv[2])
    prev_f_name = preproc_folder+"/pagerank_"+str(interval_id-1)+"_p.toplist"
    curr_f_name = preproc_folder+"/pagerank_"+str(interval_id)+"_c.toplist"
    if os.path.isfile(curr_f_name): # check whether the given day is empty
        top_list_prev = load_toplist(prev_f_name)
        top_list = load_toplist(curr_f_name)
        val, w_val = kendall_all(top_list_prev, top_list)
        out_f_name = preproc_folder+"/pagerank_"+str(interval_id)+".kendall"
        out_file = open(out_f_name,"w")
        out_file.write(str(val)+" "+str(w_val)+"\n")
        out_file.close()
    else:
        print "Interval "+ str(interval_id) + " is empty!"

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 3:
        main()
    else :
        print 'Usage: <preproc_folder> <interval_id>'
