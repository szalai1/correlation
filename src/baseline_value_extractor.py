#!/usr/bin/python

import sys,os
import operator
import correlation_computer_for_centrality_ranking as ccfcr

def pre_proc(centrality_data_folder, input_file_prefix, day):
    file = open(centrality_data_folder + "/" + input_file_prefix + "_" + str(day) + ".txt") # here input does not need to be sorted
    ret_val = {}
    # input files (e.g.: *.txt_s) are ordered according to centrality scores
    for line in file:
        splitted = line[:-1].split(" ")
        ret_val[int(splitted[0])] = float(splitted[1])
    return ret_val

def baseline_1(day_data_maps, lookback, interval_id):
	out_map = {}
	for vertex in day_data_maps[interval_id]:
		v_sum = 0.0
		for i in range(1,lookback+1):
			if vertex in day_data_maps[interval_id - i]:
				v_sum += day_data_maps[interval_id - i][vertex]
		out_map[vertex] = float(v_sum) / lookback
	return out_map

def baseline_2(day_data_maps, lookback, interval_id):
	out_map = {}
	for vertex in day_data_maps[interval_id]:
		v_sum = 0.0
		v_count = 0
		for i in range(1,lookback+1):
			if vertex in day_data_maps[interval_id - i]:
				v_sum += day_data_maps[interval_id - i][vertex]
				v_count += 1
		if v_count > 0:
			out_map[vertex] = float(v_sum) / v_count
		else:
			out_map[vertex] = 0.0
	return out_map

def eval_and_sort_days(day_data_maps, lookback, baseline_eval):
	out_maps = []
	for i in range(lookback, len(day_data_maps)):
		evaled = baseline_eval(day_data_maps, lookback, i)
		out_maps.append(sorted(evaled.items(), key=operator.itemgetter(1), reverse=True))
	return out_maps

def write_out(output_folder, input_file_prefix, baseline_type, sorted_day_data_map, counter):
	out_file = open(output_folder + "/" + input_file_prefix + "_baseline" + str(baseline_type) + "_" + str(counter) + ".txt_s", 'w')
	for i in sorted_day_data_map:
			out_file.write(str(i[0])+" "+str(i[1])+"\n")
	out_file.close()

def main():
    centrality_data_folder = sys.argv[1]
    input_file_prefix = sys.argv[2]
    lookback = int(sys.argv[3])
    baseline_type = int(sys.argv[4])
    output_folder = sys.argv[5]
    intervals = ccfcr.load_json(centrality_data_folder)
    day = 0
    day_data_maps = []

    processed_indices = []
    index_counter = 0
    for inter in intervals["centrality_test"]["intervals"]:
        print("[preproc day = " + str(day) +" ]")
        if  inter["interval"]["graph_stat"]["num_nodes"] != 0:
            day_data_maps.append(pre_proc(centrality_data_folder, input_file_prefix, day))
            if day >= lookback:
                processed_indices.append(index_counter)
                index_counter += 1
            else:
                processed_indices.append(-1)
        else:
            print "empty day"
            processed_indices.append(-1)
        day+=1
    #print day_data_maps
    #print processed_indices

    print "evaluating baseline STARTED"
    if baseline_type == 1:
    	processed_day_maps = eval_and_sort_days(day_data_maps, lookback, baseline_1)
    elif baseline_type == 2:
    	processed_day_maps = eval_and_sort_days(day_data_maps, lookback, baseline_2)
    else:
    	print "ERROR: baseline_type must be 1 or 2!"
    	return
    #print processed_day_maps

    for i in range(0, len(processed_indices)):
        #print str(processed_indices[i])
        if processed_indices[i] == -1:
            continue
        else:
    	   write_out(output_folder, input_file_prefix, baseline_type, processed_day_maps[processed_indices[i]], i)
    print "evaluating baseline FINISHED"

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 6:
        main()
    else:
        print 'Usage: <centrality_data_folder> <input_file_prefix> <lookback> <baseline_type> <output_folder>'