import operator
import sys

def main():
    in_file = open(sys.argv[1])
    out_file = open(sys.argv[2],'w')
    x = {}
    for i in in_file:
        splitted = i.split(" ")
        x[splitted[0]] = float(splitted[1])
    in_file.close()
    sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
    for i in sorted_x:
        out_file.write(i[0]+" "+str(i[1])+"\n")

if __name__ == '__main__':
    main()
