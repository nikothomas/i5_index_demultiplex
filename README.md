# Custom amplicon library demultiplexing scripts for the illumina i5 index

Demultiplexes reads from our amplicon libraries based on an 8bp i5 index that follows 4 degenerate bases. Reads should already be demultiplexed based on the i7 index.

## Instructions

1. Create a tab-delimited file that has the samples, beginning of filename for the i7-demultiplixed fastqs, and the barcode information. See demux.tsv. In the example, the fastq files would be pool1-group1_S1_L001_R1_001.fastq and pool1-group1_S1_L001_R2_001.fastq.

2. Run python run_demultiplex.py <demux_file>
