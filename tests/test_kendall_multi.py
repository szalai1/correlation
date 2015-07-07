import sys, os, math
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import correlation_computer_for_centrality_ranking as ccfcr
import kendall_multi_computer as kmc

epsilon = 0.0001

# Similar ranked lists
prev_data = {0:0.03, 1:0.02, 2:0.018}
sorted_prev_data = sorted(prev_data, reverse=True)
curr_data = {1:0.05, 0:0.04, 2:0.01}
sorted_ids = [1,0,2]

def test_kendall_tau_all():
	assert abs(ccfcr.kendall_tau(prev_data, curr_data) - kmc.kendall_tau_all(prev_data, curr_data, sorted_prev_data)[0]) < epsilon # original
	assert abs(ccfcr.kendall_tau_w(prev_data, curr_data) - kmc.kendall_tau_all(prev_data, curr_data, sorted_prev_data)[1]) < epsilon # weighted
	assert abs(ccfcr.kendall_tau(sorted_prev_data, sorted_prev_data) - kmc.kendall_tau_all(prev_data, curr_data, sorted_prev_data)[2]) < epsilon # original for list_a
	assert abs(ccfcr.kendall_tau_w(sorted_prev_data, sorted_prev_data) - kmc.kendall_tau_all(prev_data, curr_data, sorted_prev_data)[3]) < epsilon # weighted for list_a
	assert abs(ccfcr.kendall_tau(curr_data, curr_data) - kmc.kendall_tau_all(prev_data, curr_data, sorted_prev_data)[4]) < epsilon # original for list_b
	assert abs(ccfcr.kendall_tau_w(curr_data, curr_data) - kmc.kendall_tau_all(prev_data, curr_data, sorted_prev_data)[5]) < epsilon # weighted for list_b

# Dissimilar ranked list: new nodes exists
curr_data_d = {1:0.05, 4:0.04, 5:0.01}
sorted_ids_d = [1,4,5]

def test_kendall_all():
	prev_data_full, curr_data_full = ccfcr.proc_kendall(prev_data, curr_data_d, sorted_ids_d) 
	p_res =kmc.kendall_all(prev_data_full, curr_data_full)
	c_res = ccfcr.kendall(prev_data, curr_data_d, sorted_ids_d)
	assert abs(c_res[0] - p_res[0]) < epsilon
	assert abs(c_res[1] - p_res[1]) < epsilon
