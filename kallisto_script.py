import sys, datetime, os, re
from collections import defaultdict
from itertools import groupby

def kallisto_caller(full_label, fastq_files_groups):
    printt('about to quantify {}'.format(full_label))

    sample_output_dir = results_dir + '/' + full_label
    executable = 'time kallisto quant'
    options = ' -i {} -o {} --bias -t {} -b {} {} '.format(transcriptome_index, sample_output_dir, threads, boots, strand_flag)

    for fastq_files in fastq_files_groups:
        command = executable + options + ' '.join(fastq_files)
        print('')
        print(command)
        os.system(command)
        print('')

    return None

def printt(label):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S \t {}".format(label)))
    return None

# Load Kallisto module (specific to your HPC environment)
os.system("module load kallisto")

###
### 0. user defined variables
###
clean_fastq_dir = '/users/home/jdr2/clean_fastq'
boots = 100
threads = 64
results_dir = '/users/home/jdr2/sequencing_kallisto/kallisto.{}'.format(boots)
transcriptome_index = '/users/home/jdr2/transcriptome.idx'

# Set the strand flag based on your library preparation
#strand_flag = '--rf-stranded'  # for RF stranded libraries
#strand_flag = '--fr-stranded'  # for FR stranded libraries
strand_flag = ''                # for non-strand specific libraries

###
### 1. recover labels and directories
###
printt('recover labels...')

full_labels = defaultdict(list)
for directory in os.listdir(clean_fastq_dir):
    dir_path = os.path.join(clean_fastq_dir, directory)
    if os.path.isdir(dir_path):
        for file in os.listdir(dir_path):
            match = re.match(r"(RNA_test_\d+)_EKRN\d+-\dA_[A-Z0-9]+_R[12]_clean.fastq.gz", file)
            if match:
                test_label = match.group(1)
                full_labels[test_label].append(os.path.join(dir_path, file))

###
### 2. call kallisto quant
###
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

for test_label, fastq_files in full_labels.items():
    # Group fastq files by pair (R1, R2)
    grouped_fastq_files = [sorted(g) for k, g in groupby(sorted(fastq_files), key=lambda x: x.split('_R')[0])]
    kallisto_caller(test_label, grouped_fastq_files)
