#!/bin/bash 

# execute python script to divide data.in files and insert divisions in temporary sub folders
python3 divide_data_files.py -ncpus $number_of_cpus -data_in $processing_folder/$orb/F$SS/raw -subswaths ${subswaths[@]}

# execute parallel processing with divided data.in files
find . -type f -name 'data.in' | parallel ./preproc_batch_tops.csh "{/}" $processing_folder/dem/dem.grd 2 >> $processing_folder/$orb/F$SS/raw/preproc_batch_tops_results.txt

# remove divided data.in files created and respective parent folders
find . -type d -name 'sub_preproc_batch_tops_*'| parallel rm -r {}