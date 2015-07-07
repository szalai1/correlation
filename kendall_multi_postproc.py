import json
import sys
import correlation_computer_for_centrality_ranking as ccfcr
    
def load_json(dirname):
    file_name = dirname + "/intervals.json"
    file = open(file_name)
    return json.load(file)

def load_partial_results(day):
    result_f_name = sys.argv[2] + '/pagerank_'+str(day)+".kendall"
    f = open(result_f_name)
    for line in f: # there is only one line line in each file
       splitted = line[:-1].split(" ")
    return [splitted[0], splitted[1]]

def main():
    intervals = load_json(sys.argv[1])
    out_file = open(sys.argv[3], 'w')
    day = 0
    num_nodes = 1
    for inter in intervals["centrality_test"]["intervals"]:
        print("[ day = " + str(day) +" ]")
        if  inter["interval"]["graph_stat"]["num_nodes"] != 0:
            num_prev_nodes = num_nodes
            num_nodes = inter["interval"]["graph_stat"]["num_nodes"]
        else:
            out_file.write(str(inter["interval"]["time"]["start"])+" - - 0 -1.0 -1.0\n")
            day+=1
            continue
        if day != 0:
            centralities = [str(inter["interval"]["time"]["start"])]
            centralities += load_partial_results(day)
            num_new_nodes = inter["interval"]["graph_stat"]["new_nodes"]
            num_deleted_nodes = inter["interval"]["graph_stat"]["deleted_nodes"]
            centralities.append(num_nodes)
            centralities.append(float(num_new_nodes) / num_nodes)
            centralities.append(float(num_deleted_nodes)/ num_prev_nodes)
            ccfcr.write_out(out_file, centralities)
        day+=1
        
if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 4:
        main()
    else:
        print 'Usage: <centrality_data_folder> <preproc_folder> <output_file>'
