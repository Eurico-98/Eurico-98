import os
import pathlib as pl
import argparse


def divide_data_in(number_of_cpus, data_in, number_of_subswath):

    sub_folder_number_ID = 0 # to name temporary sub folders
    
    data_file = open(data_in, "r")

    # get total lines in data.in subtrat the first line that will be present in all sub files
    data_total_lines = sum(1 for line in open(data_in)) - 1

    # get list of lines from data.in
    data_lines = data_file.readlines()
    position = 1 # line index

    # get first line from data.in that represents the master file
    master_file = data_lines[0]

    # get total number of sub processes rouded down 
    n_subprocess = number_of_cpus//number_of_subswath
    

    # -------------------------  get total lines for each division of data.in -------------------------
    
    # if number of subprocesses is lower than total lines
    if(n_subprocess < data_total_lines):
        n_lines_in_sub_file = data_total_lines // n_subprocess # floor division
        n_remainder_lines = data_total_lines % n_subprocess # get remainder lines
        
        # add the remainder of cpus to n_subprocesses
        # this way avoids overloading remainder of cpus with too much work
        n_subprocess += number_of_cpus%number_of_subswath
        remainder_of_cpus = number_of_cpus%number_of_subswath # get remainder of cpus

        # if there are cpus remaining but there aren't lines remaining subtract extra unecessary cpus
        if(remainder_of_cpus > 0 and n_remainder_lines == 0):
            n_subprocess -= remainder_of_cpus

        # if the number os subprocessees is bigger or qual to the number os lines to process each sub process gets only 1 line
                
        # --------------------------------------------------------------------------------------------------
    
        # loop through all sub processes
        for subprocess in range(n_subprocess):
        
            # create sub folder do execute sub processes
            path_to_temp_subfolder = 'sub_preproc_batch_tops_{}'.format(sub_folder_number_ID)
            sub_folder_number_ID += 1

            if not os.path.exists(path_to_temp_subfolder):
                os.mkdir(path_to_temp_subfolder)

            # get new file path
            new_file_path = os.path.join(path_to_temp_subfolder, 'data.in')

            # create sub files from data.in
            new_file = open(new_file_path, 'w')

            # copy first line from data.in
            new_file.write(master_file)

            # only needed if number of subprocesses is lower than total lines to process
            if(n_subprocess < data_total_lines):
                
                if(remainder_of_cpus > 0):
                            
                    if(n_remainder_lines == 0):
                        # if cpus remain and NO lines remain -> each sub file gets the same amount of lines and remaning cpus aren't used
                        new_file.writelines( data_lines[ position:(position+n_lines_in_sub_file) ] )
                    
                    elif(subprocess < n_subprocess-1):
                        # if cpus remain and lines remain but it is not the last iteration -> each sub file gets the same amount of lines
                        new_file.writelines( data_lines[ position:(position+n_lines_in_sub_file) ] )
                    
                    else:
                        # if cpus remain and lines remain and it is the last iteration -> the last sub file will get the remainder of the lines and the remainder of cpus will process that file
                        new_file.writelines( data_lines[ position:(position+n_remainder_lines) ] )

                # if ther are NO cpus remaining and no lines remain -> each sub file gets the same amount of lines                        
                elif(n_remainder_lines == 0):
                    new_file.writelines( data_lines[ position:(position+n_lines_in_sub_file) ] )

                # if ther are NO cpus remaining but there are lines remain and it is not the last iteration -> each sub file gets the same amount of lines                    
                elif(subprocess < n_subprocess-1):
                    new_file.writelines( data_lines[ position:(position+n_lines_in_sub_file) ] )
                
                # if ther are NO cpus remaining and lines remain -> and it is the last iteration add extra lines to last file
                else:
                    new_file.writelines( data_lines[ position:(position + n_lines_in_sub_file + n_remainder_lines) ] )
                
                # increment position indicator
                position += n_lines_in_sub_file
            
            else:
                new_file.writelines( data_lines[ position ] )      
                
                # increment position indicator
                position += 1  
                
                # break when all lines have been inserted in a sub file
                if(len(data_lines) == position):
                    break  
                    
            new_file.close()

    data_file.close()


if __name__ == "__main__":
    
    # set parser
    parser = argparse.ArgumentParser(description='''
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
    divide_data_files -ncpus 64  -data_in (...)/F1/raw/data.in  -subswaths 3''')
    
    # set arguments
    parser.add_argument('-ncpus', '--ncpus', metavar='', required=True, help='insert valid number of cpus')
    parser.add_argument('-data_in', '--data_in', metavar='', required=True, help='insert valid path for data.in files')
    parser.add_argument('-subswaths', '--subswaths', metavar='', required=True, help='inser number of subswaths to use')
    args = parser.parse_args()
    
    
    divide_data_in(int(args.ncpus), args.data_in, int(args.subswaths))