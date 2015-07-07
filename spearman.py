import math
import json
import sys

def pre_proc(day): # there are no ties in this case!
    file = open(sys.argv[1]+ "/pagerank_scores_" + str(day) + ".txt_s")
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
    intervals = load_json(sys.argv[1])
    out_file = open(sys.argv[2], 'w')
    day = 0
    top_list_prev = []
    top_list = []
    ret_sort = []
    for inter in intervals["centrality_test"]["intervals"]:
        print("[ day = " + str(day) +" ]")
        if  inter["interval"]["graph_stat"]["num_nodes"] != 0:
            #top_list, ret_sort = pre_proc(day)
            top_list = pre_proc(day)
        else:
            out_file.write(str(inter["interval"]["time"]["start"])+" - 0\n")
            day+=1
            continue
        if day != 0:
            centralities  = spearman(top_list_prev, top_list)#, ret_sort)
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
