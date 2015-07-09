import sys
import correlation_computer_for_centrality_ranking as ccfcr
import correlation_computer_for_position_ranking as ccfpr

#########################

def kendall_printer(list_prev, list_curr):
	print "================="
	print "kendall test:"
	print "list_prev: " + str(list_prev)
	print "list_curr: " + str(list_curr)
	print "kendall_: " + str(ccfcr.compute_kendall(list_prev, list_curr)[0])
	print "kendall_w: " + str(ccfcr.compute_kendall(list_prev, list_curr)[1])
	print "================="
	print

def correlation_printer(list_prev, list_curr):
	print "================="
	print "correlation test:"
	print "list_prev: " + str(list_prev)
	print "list_curr: " + str(list_curr)
	print "corr_: " + str(ccfpr.compute_corr(list_prev, list_curr)[0])
	print "corr_w: " + str(ccfpr.compute_corr(list_prev, list_curr)[1])
	print "================="
	print

##########################

list_avg_p = [1.5, 1.5, 3.5, 3.5]
list_avg_c = [3.5, 3.5, 1.5, 1.5]

list_p = [1, 2, 3, 4]
list_c_1 = [3, 4, 1, 2]
list_c_2 = [4, 3, 1, 2]
list_c_3 = [3, 4, 2, 1]
list_c_4 = [4, 3, 2, 1]

# correlation
correlation_printer(list_avg_p, list_avg_c)
correlation_printer(list_p, list_c_1)
correlation_printer(list_p, list_c_2)
correlation_printer(list_p, list_c_3)
correlation_printer(list_p, list_c_4)
correlation_printer(list_p, list_p)


# kendall-tau
kendall_printer(list_avg_p, list_avg_c)
kendall_printer(list_p, list_c_1)
kendall_printer(list_p, list_c_2)
kendall_printer(list_p, list_c_3)
kendall_printer(list_p, list_c_4)




