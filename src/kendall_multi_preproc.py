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
    for i in value_list[1:]:
        outfile.write(str(i)+"\n")

#####################################################################
    
def load_json(dirname):
    file_name = dirname + "/intervals.json"
    file = open(file_name)
    return json.load(file)

def main():
    centrality_data_folder = sys.argv[1]
    intervals = load_json(centrality_data_folder)
    file_prefix = sys.argv[2]
    out_folder = sys.argv[3]
    day = 0
    top_list_prev = []
    top_list = []
    ret_sort = []
    num_nodes = 1
    for inter in intervals["centrality_test"]["intervals"]:
        print("[preproc day = " + str(day) +" ]")
        if  inter["interval"]["graph_stat"]["num_nodes"] != 0:
            top_list, ret_sort = ccfcr.pre_proc(centrality_data_folder, file_prefix, day)
        else:
            print str(day) + ": empty"
            day+=1
            continue
        if day != 0:
            full_prev_toplist, full_toplist = ccfcr.proc_kendall(top_list_prev, top_list, ret_sort)
            write_out_toplists(out_folder+"/pagerank_", day, full_prev_toplist, full_toplist)
        day+=1
        top_list_prev = top_list
        
if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 4:
        main()
    else:
        print 'Usage: <centrality_data_folder> <file_prefix> <preproc_folder>'