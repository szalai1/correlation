#!/usr/bin/python

import os,sys
import correlation_computer_for_centrality_ranking as ccfcr
import correlation_computer_for_position_ranking as ccfpr

argc = len(sys.argv)
if argc == 10:
	input_file_folder_1 = sys.argv[1] # for baseline
	file_prefix_1 = sys.argv[2] # for balseline
	input_file_folder_2 = sys.argv[3] # for origi
	file_prefix_2 = sys.argv[4] # for origi
	from_interval = int(sys.argv[5])
	to_interval = int(sys.argv[6])
	rank_type = sys.argv[7]
	output_file = sys.argv[8]
	metric = sys.argv[9]
	
	intervals = ccfcr.load_json(input_file_folder_2)
	out_file = open(output_file, 'w')
	top_list_other = []
	top_list = []
	ret_sort = []
	intervals_list = intervals["centrality_test"]["intervals"]
	for day in range(from_interval, to_interval+1):
		print("[ day = " + str(day) +" ]")
		if  intervals_list[day]["interval"]["graph_stat"]["num_nodes"] != 0:
			if rank_type == "centrality":
				top_list_other, ret_sort_other = ccfcr.pre_proc(input_file_folder_1, file_prefix_1, day) # for baseline
				top_list, ret_sort = ccfcr.pre_proc(input_file_folder_2, file_prefix_2, day) # for origi
			elif rank_type == "pos":
				top_list_other, ret_sort_other = ccfpr.pre_proc(input_file_folder_1, file_prefix_1, day) # for baseline
				top_list, ret_sort = ccfpr.pre_proc(input_file_folder_2, file_prefix_2, day) # for origi
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
	print 'Usage: <input_file_folder_1> <file_prefix_1> <input_file_folder_2> <file_prefix_2> <from_interval> <to_interval> <centrality/pos> <output_file> <kendall/corr>'