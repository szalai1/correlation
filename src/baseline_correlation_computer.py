#!/usr/bin/python

import os,sys
import correlation_computer_for_centrality_ranking as ccfcr
import correlation_computer_for_position_ranking as ccfpr

argc = len(sys.argv)
if argc == 10:
	baseline_folder = sys.argv[1] # for baseline
	centrality_folder = sys.argv[2] # for origi
	file_prefix = sys.argv[3]
	baseline_type = sys.argv[4]
	from_interval = int(sys.argv[5])
	to_interval = int(sys.argv[6])
	rank_type = sys.argv[7]
	metric = sys.argv[8]
	output_file = sys.argv[9]
	
	intervals = ccfcr.load_json(centrality_folder)
	out_file = open(output_file, 'w')
	top_list_other = []
	top_list = []
	ret_sort = []
	intervals_list = intervals["centrality_test"]["intervals"]
	for day in range(from_interval, to_interval+1):
		print("[ day = " + str(day) +" ]")
		if  intervals_list[day]["interval"]["graph_stat"]["num_nodes"] != 0:
			if rank_type == "centrality":
				top_list_other, ret_sort_other = ccfcr.pre_proc(baseline_folder, file_prefix + "_baseline" + baseline_type, day) # for baseline
				top_list, ret_sort = ccfcr.pre_proc(centrality_folder + "/centrality_scores", file_prefix, day) # for origi
			elif rank_type == "pos":
				top_list_other, ret_sort_other = ccfpr.pre_proc(baseline_folder, file_prefix + "_baseline" + baseline_type, day) # for baseline
				top_list, ret_sort = ccfpr.pre_proc(centrality_folder + "/centrality_scores", file_prefix, day) # for origi
			else:
				print "rank_type must be 'centrality' or 'pos'!!!"
		else:
			out_file.write(str(day)+" - -\n")
			continue
		#print top_list_other
		#print
		#print top_list
		if day != 0:
			centralities = [str(day)]
			if rank_type == "centrality":
				centralities += ccfcr.compute(top_list_other, top_list, ret_sort, metric)
			elif rank_type == "pos":
				centralities += ccfpr.compute(top_list_other, top_list, ret_sort, metric)
			else:
				print "rank_type must be 'centrality' or 'pos'!!!"
			ccfcr.write_out(out_file, centralities)

else:
	print 'Usage: <baseline_folder> <original_input_file_folder> <file_prefix> <baseline_type> <from_interval> <to_interval> <centrality/pos> <kendall/corr> <output_file>'