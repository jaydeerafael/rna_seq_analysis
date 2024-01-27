import os, datetime, sys, shutil

def printt(label):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S \t {}".format(label)))
    return None

def log_to_file(log_file, message):
    with open(log_file, "a") as file:
        file.write(message + "\n")
        
        
def trimmomatic_caller(file_name_1, file_name_2, raw_fastq_dir, log_file):
    # Extract sample name from first file name
    sample = file_name_1.split('_L2_')[0]

    executable='time java -jar "/users/home/jdr2/Trimmomatic-0.39/trimmomatic-0.39.jar" PE -threads {} -phred33 '.format(number_threads)
    options = ' ILLUMINACLIP:"{}":2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36'.format(adapter_file)

    # Construct input file paths
    input1 = '"' + raw_fastq_dir + '/' + file_name_1 + '"'
    input2 = '"' + raw_fastq_dir + '/' + file_name_2 + '"'

    output_dir = clean_fastq_dir + '/' + sample + '/'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    output1 = '"' + output_dir + sample + '_R1_clean.fastq.gz' + '"'
    output2 = '"' + output_dir + sample + '_R2_clean.fastq.gz' + '"'
    garbage1 = '"' + output_dir + sample + '_R1_garbage.fastq.gz' + '"'
    garbage2 = '"' + output_dir + sample + '_R2_garbage.fastq.gz' + '"'

    input_files = input1 + ' ' + input2
    output_files = output1 + ' ' + garbage1 + ' ' + output2 + ' ' + garbage2

    command = executable + input_files + ' ' + output_files + options

    printt('about to clean {}'.format(sample))
    log_to_file(log_file, 'about to clean {}'.format(sample))
    print('')
    print(command)
    print('')
    os.system(command)
    print('')
    
    # Capture command output
    command_output = os.popen(command).read()
    print(command_output)
    log_to_file(log_file, command_output)

    return None

# User defined variables
raw_fastq_dir = '/users/home/jdr2/raw_fastq'
clean_fastq_dir = '/users/home/jdr2/clean_fastq'
trimmomatic_path = '/users/home/jdr2/Trimmomatic-0.39'
adapter_file = trimmomatic_path + 'adapters/TruSeq3-PE-2.fa'
number_threads = 24 
log_file = '/users/home/jdr2/trimmomatic_log.txt'  # Path for the log file


# Ensure the clean_fastq directory exists
if not os.path.exists(clean_fastq_dir):
    os.makedirs(clean_fastq_dir)

# Recover samples
all_files = os.listdir(raw_fastq_dir)
samples = [(f, f.replace('_L2_1.fq.gz', '_L2_2.fq.gz')) for f in all_files if '_L2_1.fq.gz' in f]

# Iterate Trimmomatic
for file_name_1, file_name_2 in samples:
    trimmomatic_caller(file_name_1, file_name_2, raw_fastq_dir, log_file)
