#!/usr/bin/python

import sys, os, math
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import correlation_computer_for_centrality_ranking as ccfcr
import correlation_computer_for_position_ranking as ccfpr

epsilon = 0.0001

def test_yana_formula():
	n=100
	num = 0.0
	for i in range(n):
		num += math.pow(i+1,2)
	res = num / n - math.pow(n+1,2) / 4
	assert res == (math.pow(n,2) - 1) / 12 
	#assert res == ccfpr.correl_var(n,1.0)

def test_avg():
	assert ccfcr.avg([1,2,3,4,5]) == ccfcr.avg([1,2.5,2.5,4.5,4.5])

# Similar ranked lists
prev_data_with_position = [1,2,3]
prev_data_with_position_reverse = [3,2,1]
curr_data_with_position = [2,1,3]
sorted_ids = [1,0,2]
s = ccfcr.szum(3)

def test_correl():
	val = ccfcr.correl(prev_data_with_position, curr_data_with_position, s)
	val_pos = ccfpr.correl(prev_data_with_position, curr_data_with_position, s)[0]
	assert abs(val - val_pos) < epsilon

def test_correl_var():
	n=100
	l = range(1,n+1)
	s_n = ccfcr.szum(n)
	val = ccfcr.correl(l, l, s_n)
	val_pos = ccfpr.correl_var(n, s_n)[0]
	assert abs(val - val_pos) < epsilon	

def test_correl_w():
	val = ccfcr.correl_w(prev_data_with_position, curr_data_with_position, s)
	val_pos = ccfpr.correl(prev_data_with_position, curr_data_with_position, s)[1]
	assert abs(val - val_pos) < epsilon

def test_correl_w_var():
	n=100
	l = range(1,n+1)
	s_n = ccfcr.szum(n)
	val = ccfcr.correl_w(l, l, s_n)
	val_pos = ccfpr.correl_var(n, s_n)[1]
	assert abs(val - val_pos) < epsilon	

"""
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

# special: small test 2: it is a synthetic exmaple
prev_c_2 = {2:0.131812, 1:0.07125, 0:0.05}
prev_p_2 = {2:1, 1:2, 0:3}
curr_c_2 = {3:0.123921, 4:0.069375, 2:0.0669844, 1:0.0375}
curr_p_2 = {3:1, 4:2, 2:3, 1:4}
sorted_ids_small_2 = [3,4,2,3]

def test_kendall_small_2(): # there is no tie!
	cres = ccfcr.kendall(prev_c_2, curr_c_2, sorted_ids_small_2)
	print cres
	pres =ccfpr.kendall(prev_p_2, curr_p_2, sorted_ids_small_2)
	print pres
	assert abs(cres[0] - pres[0]) < epsilon
	assert abs(cres[1] - pres[1]) < epsilon

# special: small test: it is a synthetic exmaple
prev_c = {2:0.329029, 1:0.32495, 3:0.136107, 4:0.00015015, 5: 0.00015015, 6: 0.00015015}
prev_p = {2:1, 1:2, 3:3, 4:4, 5:4, 6:4}
curr_c = {2:0.329029, 1:0.32495, 3:0.136234, 7:0.00015015, 8: 0.00015015, 9: 0.00015015}
curr_p = {2:1, 1:2, 3:3, 7:4, 8:4, 9:4}
sorted_ids_small = [2,1,3,7,8,9]

def test_kendall_small(): # there are ties!
	cres = ccfcr.kendall(prev_c, curr_c, sorted_ids_small)
	print cres
	pres =ccfpr.kendall(prev_p, curr_p, sorted_ids_small)
	print pres
	assert abs(cres[0] - pres[0]) < epsilon
	assert abs(cres[1] - pres[1]) < epsilon
"""