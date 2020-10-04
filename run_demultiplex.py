#!/usr/bin/env python
#
# Usage: python run_demultiplex.py <demux_file>
#
import sys, os

manifest_handle = open(sys.argv[1])

line_number = 0
while 1:
        line_number = line_number + 1
        line = manifest_handle.readline()
        if not line:
            break
        line = line.rstrip()
            
        name, file_name, idx1, seq1, idx2, seq2 = line.split("\t")
        if line_number > 1:
            if os.path.isfile(file_name + "_R1_001.fastq") and os.path.isfile(file_name + "_R2_001.fastq"):
                os.system("./fastq_demultiplexF4N8I.pl " + 
                  file_name + "_R1_001.fastq " + 
                  file_name + "_R2_001.fastq " + 
                  seq2 + " " + 
                  name + "_" + seq2 +
                  " 2>> logfile.txt")
            else:
                print ("file(s) do not exist: " + file_name)



