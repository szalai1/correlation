#!/usr/bin/python

import math, json, sys, os
import correlation_computer_for_centrality_ranking as ccfcr

################################ FELDOLGOZOK ############################
def write_out_toplists(prefix, append, full_prev_list, full_current_list):
    prev_f_name = prefix+str(append-1)+"_p.toplist"
    prev_file = open(prev_f_name, 'w')
    write_toplist(prev_file, full_prev_list)
    prev_file.close()
    curr_f_name = prefix+str(append)+"_c.toplist"
    curr_file = open(curr_f_name, 'w')
    write_toplist(curr_file, full_current_list)
    curr_file.close()

def write_toplist(outfile, value_list):
    for i in value_list[0:]:
        outfile.write(str(i)+"\n")

#####################################################################
    
def load_json(dirname):
    file_name = dirname + "/intervals.json"
    file = open(file_name)
    return json.load(file)

def main():
    baseline_folder = sys.argv[1] # for baseline
    centrality_folder = sys.argv[2] # for origi
    file_prefix = sys.argv[3]
    baseline_type = sys.argv[4]
    from_interval = int(sys.argv[5])
    to_interval = int(sys.argv[6])
    out_folder = sys.argv[7]
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    intervals = load_json(centrality_folder)
    top_list_other = []
    top_list = []
    ret_sort = []
    intervals_list = intervals["centrality_test"]["intervals"]
    for day in range(from_interval, to_interval+1):   
        print("[preproc day = " + str(day) +" ]")
        if  intervals_list[day]["interval"]["graph_stat"]["num_nodes"] != 0:
            top_list_other, ret_sort_other = ccfcr.pre_proc(baseline_folder, file_prefix + "_baseline" + baseline_type, day) # for baseline
            top_list, ret_sort = ccfcr.pre_proc(centrality_folder + "/centrality_scores", file_prefix, day) # for origi
        else:
            print str(day) + ": empty"
            day+=1
            continue
        if day != 0:
            full_prev_toplist, full_toplist = ccfcr.proc_kendall(top_list_other, top_list, ret_sort)
            write_out_toplists(out_folder + "/" + file_prefix + "_", day, full_prev_toplist, full_toplist)
        
if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 8:
        main()
    else:
        print 'Usage: <baseline_folder> <original_input_file_folder> <file_prefix> <baseline_type> <from_interval> <to_interval> <preproc_folder>'