#!/usr/bin/python

import sys

FILE_DELIMITER = ","

def process_file(input_f, from_index, to_index, output_prefix):
	f_in = open(input_f, 'r')
	line_num = 1
	for line in f_in:
		if line_num >= from_index and line_num <= to_index:
			f_out = open(output_prefix + "_" + str(line_num-1) + ".txt", 'w')
			splitted = line.rstrip().split(FILE_DELIMITER)
			for i in range(len(splitted)):
				f_out.write(str(i+1) + " " + splitted[i] + "\n")
			f_out.close()
			line_num += 1
	f_in.close()


if __name__ == "__main__":
	argc = len(sys.argv)
	if argc == 5:
		input_file = sys.argv[1]
		from_days = int(sys.argv[2])
		to_days = int(sys.argv[3])
		output_file_prefix = sys.argv[4]
		process_file(input_file, from_days, to_days, output_file_prefix)
	else:
		print "Usage: <input_file> <from_days> <to_days> <output_file_prefix>"  