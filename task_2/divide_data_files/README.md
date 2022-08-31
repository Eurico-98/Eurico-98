In this branch the changes from the main branch, made by Eurico-98, are in the automation.sh file in the lines from 248 to 255:

	# execute python script to divide data.in files and insert divisions in temporary sub folders
	docker run -it -v $scripts_folder/processing_tools/divide_data_files:/processing_folder --rm divide_data_files -ncpus $number_of_cpus -data_in $processing_folder/$orb/F$SS/raw -subswaths ${subswaths[@]}

	# execute parallel processing with divided data.in files
    find . -type f -name 'data.in' | parallel preproc_batch_tops.csh "{/}" $processing_folder/dem/dem.grd 2 >>                  $processing_folder/$orb/F$SS/raw/preproc_batch_tops_results.txt

	# remove divided data.in files created and respective parent folders
	find . -type d -name 'sub_preproc_batch_tops_*'| parallel rm -r {}


Moreover the srcipt used here is in the location:

GMTSAR_SBAS_AUTOMATION/processing_tools/divide_data_files

What the script does is:

    Execute parallel processing of preproc_batch_tops.csh
    
    First divides data.in file like so:
    
    if there are 3 cpus and 31 lines inside the data.in creates 3 sub folders:
    
    sub_preproc_batch_tops_0
            '- data.in  -> with 10 lines
    sub_preproc_batch_tops_1
            '- data.in  -> with 10 lines
    sub_preproc_batch_tops_2
            '- data.in  -> with 10 lines
    each data.in has the same first line that refers to the master
    
    Example input:
    divide_data_files -ncpus 64  -data_in (...)/F1/raw/data.in  -subswaths 3'''
    
