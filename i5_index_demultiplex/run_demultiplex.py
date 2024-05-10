#!/usr/bin/env python
#
# Usage: python run_demultiplex.py <demux_file>
#
import os
import gzip
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import shutil

os.chdir('..')
os.chdir('./Metadata')

# Get a list of all files in the current directory
files = os.listdir()

# Filter Excel files based on the .txt or .tsv extension and 'barcodes' in the file name
excel_files = [file for file in files if file.endswith('.txt') or file.endswith('.tsv') and 'barcodes' in file]

manifest_handle = open(excel_files[0])
os.chdir('..')
os.chdir('./Raw Sequences')
# Gzip FASTQ files in the "Raw Sequences" directory
# Create the '../i5_demultiplexed_sequences' directory if it doesn't exist
demux_dir = '../Demultiplexed Sequences'
os.makedirs(demux_dir, exist_ok=True)
progress = 0
num_processed = 0
def process_line(barcode_line):
    global num_processed
    global progress
    name, file_name, idx1, seq1, idx2, seq2 = barcode_line.split("\t")
    if os.path.isfile(file_name + "_R1_001.fastq") and os.path.isfile(file_name + "_R2_001.fastq"):
        os.system("../i5_index_demultiplex/fastq_demultiplexF4N8I.pl " +
                  file_name + "_R1_001.fastq " +
                  file_name + "_R2_001.fastq " +
                  seq2 + " " +
                  name + "_" + seq2 +
                  " 2>> ../logs/i5_index_demultiplex_log.txt")
        print(f"\rProgress: [{'#' * int(progress / 2)}{'-' * (50 - int(progress / 2))}] {progress:.2f}%", end='', flush=True)
        # Rename and move the demultiplexed files to the '../i5_demultiplexed_sequences' directory
        for file in os.listdir():
            if file.startswith(name + "_" + seq2):
                if file.endswith("_R1.fastq"):
                    new_file_name = f"{name}_{seq2}_L001_R1_001.fastq"
                elif file.endswith("_R2.fastq"):
                    new_file_name = f"{name}_{seq2}_L001_R2_001.fastq"
                else:
                    continue

                # Compress the file using gzip and move it to the '../i5_demultiplexed_sequences' directory
                with open(file, 'rb') as f_in:
                    with gzip.open(os.path.join(demux_dir, new_file_name + '.gz'), 'wb') as f_out:
                        f_out.writelines(f_in)
                # Remove the original uncompressed file
                os.remove(file)
    else:
        print("File(s) do not exist: " + file_name)


line_number = 0
lines = []
while 1:
    line_number = line_number + 1
    line = manifest_handle.readline()
    if not line:
        break
    line = line.rstrip()
    if line_number > 1:
        lines.append(line)

for line in lines:
    process_line(line)
    num_processed += 1
    progress = num_processed / len(lines) * 100
    print(f"\rProgress: [{'#' * int(progress / 2)}{'-' * (50 - int(progress / 2))}] {progress:.2f}%", end='', flush=True)
