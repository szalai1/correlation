#!/usr/bin/python

import math
import json
import sys
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
    input_file_folder_1 = sys.argv[1] # for baseline
    file_prefix_1 = sys.argv[2] # for balseline
    input_file_folder_2 = sys.argv[3] # for origi
    file_prefix_2 = sys.argv[4] # for origi
    from_interval = int(sys.argv[5])
    to_interval = int(sys.argv[6])
    out_folder = sys.argv[7]

    intervals = load_json(input_file_folder_2)
    top_list_other = []
    top_list = []
    ret_sort = []
    intervals_list = intervals["centrality_test"]["intervals"]
    for day in range(from_interval, to_interval+1):   
        print("[preproc day = " + str(day) +" ]")
        if  intervals_list[day]["interval"]["graph_stat"]["num_nodes"] != 0:
            top_list_other, ret_sort_other = ccfcr.pre_proc(input_file_folder_1, file_prefix_1, day) # for baseline
            top_list, ret_sort = ccfcr.pre_proc(input_file_folder_2, file_prefix_2, day) # for origi
        else:
            print str(day) + ": empty"
            day+=1
            continue
        print top_list_other
        print
        print top_list
        if day != 0:
            full_prev_toplist, full_toplist = ccfcr.proc_kendall(top_list_other, top_list, ret_sort)
            print full_prev_toplist
            print
            print full_toplist
            write_out_toplists(out_folder+"/pagerank_", day, full_prev_toplist, full_toplist)
        
if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 8:
        main()
    else:
        print 'Usage: <input_file_folder_1> <file_prefix_1> <input_file_folder_2> <file_prefix_2> <from_interval> <to_interval> <preproc_folder>'