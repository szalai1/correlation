import math
import json
import sys

def spearman(top_list_prev, top_list, sort_id):
    list_a, list_b = proc_kendall(top_list_prev, top_list, sort_id)
    
    print "### full_interval_0 ###"
    print list_a
    print
    print "### full_interval_1 ###"
    print list_b
    print len(list_a)
    print len(list_b)

    size = len(list_a)
    ret_val = 0.0
    for i in range(size):
        ret_val += list_a[i]*list_b[i]

    x =(ret_val/size) - math.pow((size + 1)/2.0, 2)
    y = (size*size-1)/12.0
    return [x/y]

def proc_kendall(l1, l2, sort_id):
    print("kendall lista")
    list_a = []
    list_b = []
    n1 = len(l1) + 1.0
    n2 = len(l2) + 1.0
    for i in sort_id:
        list_b.append(l2[i])
        if i in l1:
            list_a.append(l1[i])
        else:
            list_a.append(n1) # tie on last position
            n1 += 1
    for i in l1:
        if i not in l2:
            list_b.append(n2) # tie on last position
            n2 += 1
            list_a.append(l1[i])
    return list_a, list_b

def pre_proc(day): # there are no ties in this case!
    file = open(sys.argv[1]+ "/pagerank_scores_" + str(day) + ".txt_s")
    ret_val = {}
    ret_sort = []
    rank = 1.0
    for line in file:
        #print rank     
        splitted = line[:-1].split(" ")
        ret_val[int(splitted[0])] = rank
        rank += 1
        ret_sort.append(int(splitted[0]))
    return ret_val, ret_sort

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
    intervals = load_json(sys.argv[1])
    out_file = open(sys.argv[2], 'w')
    day = 0
    top_list_prev = []
    top_list = []
    ret_sort = []
    for inter in intervals["centrality_test"]["intervals"]:
        print("[ day = " + str(day) +" ]")
        if  inter["interval"]["graph_stat"]["num_nodes"] != 0:
            top_list, ret_sort = pre_proc(day)
        else:
            out_file.write(str(inter["interval"]["time"]["start"])+" - 0\n")
            day+=1
            continue
        if day != 0:
            centralities = spearman(top_list_prev, top_list, ret_sort)
            centralities.append( inter["interval"]["graph_stat"]["num_nodes"])
            write_out(out_file, centralities, str(inter["interval"]["time"]["start"]) )
        day+=1
        top_list_prev = top_list
                  
if __name__ == '__main__':
   argc = len(sys.argv)
   if argc == 3:
       main()
   else:
       print 'Usage: <centrality_data_folder> <output_file>'
