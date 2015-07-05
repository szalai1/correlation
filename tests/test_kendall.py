#!/usr/bin/python

import sys, os, math
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import correlation_computer_for_centrality_ranking as ccfcr
import correlation_computer_for_position_ranking as ccfpr

epsilon = 0.0001

# TODO: tie-okra is irni kene valami peldat.

# Similar ranked lists
prev_data_with_centrality = {0:0.03, 1:0.02, 2:0.018}
prev_data_with_position = {0:1, 1:2, 2:3}
prev_data_with_position_reverse = {2:1, 1:2, 0:3}
curr_data_with_centrality = {1:0.05, 0:0.04, 2:0.01}
curr_data_with_position = {1:1, 0:2, 2:3}
sorted_ids = [1,0,2]

def test_kendall_tau():
	assert abs(ccfcr.kendall_tau(prev_data_with_centrality, curr_data_with_centrality) - ccfcr.kendall_tau(prev_data_with_position, curr_data_with_position)) < epsilon
	assert False == (abs(ccfcr.kendall_tau(prev_data_with_centrality, prev_data_with_centrality) - ccfcr.kendall_tau(prev_data_with_position, curr_data_with_position)) < epsilon)

def test_kendall_tau_w():
	assert abs(ccfcr.kendall_tau_w(prev_data_with_centrality, curr_data_with_centrality) - ccfcr.kendall_tau_w(prev_data_with_position, curr_data_with_position)) < epsilon
	assert  False == (abs(ccfcr.kendall_tau_w(prev_data_with_centrality, prev_data_with_centrality) - ccfcr.kendall_tau_w(prev_data_with_position, curr_data_with_position)) < epsilon)

def test_compute_kendall():
	c_res = ccfcr.compute_kendall(prev_data_with_centrality, curr_data_with_centrality)
	p_res =ccfpr.compute_kendall(prev_data_with_position, curr_data_with_position)
	assert abs(c_res[0] - p_res[0]) < epsilon
	assert abs(c_res[1] - p_res[1]) < epsilon
	
	p_res_identity = ccfpr.compute_kendall(prev_data_with_position, prev_data_with_position)
	assert abs(p_res_identity[0]-1.0) < epsilon
	assert abs(p_res_identity[1]-1.0) < epsilon

	p_res_reverse = ccfcr.compute_kendall(prev_data_with_position, prev_data_with_position_reverse)
	assert abs(p_res_reverse[0]+1.0) < epsilon
	assert abs(p_res_reverse[1]+1.0) < epsilon

def test_kendall_similar():
	c_res = ccfcr.kendall(prev_data_with_centrality, curr_data_with_centrality, sorted_ids)
	p_res =ccfpr.kendall(prev_data_with_position, curr_data_with_position, sorted_ids)
	assert abs(c_res[0] - p_res[0]) < epsilon
	assert abs(c_res[1] - p_res[1]) < epsilon

# Dissimilar ranked list: new nodes exists
curr_data_with_centrality_d = {1:0.05, 4:0.04, 5:0.01}
curr_data_with_position_d = {1:1, 4:2, 5:3}
sorted_ids_d = [1,4,5]

def test_kendall_dissimilar():
	c_res = ccfcr.kendall(prev_data_with_centrality, curr_data_with_centrality_d, sorted_ids_d)
	c_res_2 = ccfcr.compute_kendall(prev_data_with_centrality, prev_data_with_centrality)
	p_res =ccfpr.kendall(prev_data_with_position, curr_data_with_position_d, sorted_ids_d)
	assert abs(c_res[0] - p_res[0]) < epsilon
	assert False == (abs(c_res_2[0] - p_res[0]) < epsilon)
	assert abs(c_res[1] - p_res[1]) < epsilon