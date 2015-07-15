#!/usr/bin/python

import math
import json
import sys

def pre_proc(centrality_data_folder, input_file_prefix, day):
    file = open(centrality_data_folder + "/" + input_file_prefix + "_" + str(day) + ".txt_s")
    ret_val = {}
    rank = 1.0
    for line in file:
        #print rank     
        splitted = line[:-1].split(" ")
        # rank is position! no centrality is score included.
        ret_val[int(splitted[0])] = rank
        rank += 1
    return ret_val#, ret_sort

def spearman(top_list_prev, top_list):
    ret_val = 0.0
    # potential bug!? switched variables?
    end_rank = len(top_list_prev) +1
    end_rank_prev = len(top_list) +1
    size = 0
    for i in top_list_prev:
        size += 1
        if i in top_list:
            ret_val += top_list_prev[i]*top_list[i]
        else:
            ret_val += top_list_prev[i]*end_rank_prev
            end_rank_prev += 1
            
    for i in top_list:
        if i not in top_list_prev:
            size += 1
            ret_val += top_list[i]*end_rank
            end_rank += 1

    #print end_rank_prev
    #print end_rank
    #print size

    x =(ret_val/size) - math.pow((size + 1)/2.0, 2)
    y = (size*size-1)/12.0
    return [x/y]

def write_out(outfile, value_list, time):
    outfile.write(time)
    for i in value_list:
        outfile.write(" "+ str(i))
    outfile.write("\n")
    
def load_json(dirname):
    file_name = dirname + "/intervals.json"
    file = open(file_name)
    return json.load(file)

def main():
    centrality_data_folder = sys.argv[1]
    input_file_prefix = sys.argv[2]
    output_file = sys.argv[3]
    intervals = load_json(centrality_data_folder)
    out_file = open(output_file, 'w')
    day = 0
    top_list_prev = []
    top_list = []
    ret_sort = []
    for inter in intervals["centrality_test"]["intervals"]:
        print("[ day = " + str(day) +" ]")
        if  inter["interval"]["graph_stat"]["num_nodes"] != 0:
            #top_list, ret_sort = pre_proc(day)
            top_list = pre_proc(centrality_data_folder, input_file_prefix, day)
        else:
            #out_file.write(str(inter["interval"]["time"]["start"])+" - 0\n")
            out_file.write(str(day)+" - 0\n")
            day+=1
            continue
        if day != 0:
            centralities = spearman(top_list_prev, top_list)#, ret_sort)
            centralities.append( inter["interval"]["graph_stat"]["num_nodes"])
            write_out(out_file, centralities, str(day)) #str(inter["interval"]["time"]["start"]) )
        day+=1
        top_list_prev = top_list
                  
if __name__ == '__main__':
   argc = len(sys.argv)
   if argc == 4:
       main()
   else:
       print 'Usage: <centrality_data_folder> <input_file_prefix> <output_file>'
