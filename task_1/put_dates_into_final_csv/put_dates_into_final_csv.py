import pathlib as pl
import pandas as pd
pd.options.mode.chained_assignment = None # disable false positive warning of overwriting a row in csv
import collections
from datetime import date
import argparse


# get prm and disp files
def searchFiles(file_path):
    
    # get dates and date ids returns a dictionary ordered where key is ID and value is date
    dateContent_dic = {}
    
    for path in pl.Path(file_path).iterdir():

        # read file one by one
        if path.is_file():
            
            # only add files with ALL sections of the image
            if(path.name.split("_")[2] == "ALL"):
                temp = 0
            
                # get date ID 
                current_file = open(path, "r")
                all_lines = current_file.readlines()
            
                for line in all_lines:
                
                    if line.startswith("SC_clock_start"):
                        temp = line.split("= ")[1]
                        temp = int(temp.split(".")[0])
                        break
                current_file.close()
                
                # get date from file name
                dateContent_dic[temp] = path.name.split("_")[1]
    
    # convert date to days
    for key_id, value_date in dateContent_dic.items():
                    
        d0 = date(int(value_date[0:4]), int(value_date[4:6]), int(value_date[6:8]))
        d1 = date(1,1,1)
        delta = d0 - d1
        dateContent_dic[key_id] = delta.days + 366
    
    # order dictionary by IDs from smallest to biggest
    dateContent_dic = collections.OrderedDict(sorted(dateContent_dic.items()))     
    
    return dateContent_dic
    
# insert new row in csv
def Insert_row_(row_number, df, row_value):
    
    # Slice the upper half of the dataframe
    df1 = df[0:row_number]
  
    # Store the result of lower half of the dataframe
    df2 = df[row_number:]
  
    # Insert the row in the upper half dataframe
    df1.loc[row_number]=row_value
  
    # Concat the two dataframes
    df_result = pd.concat([df1, df2])
  
    # Reassign the index labels
    df_result.index = [*range(df_result.shape[0])]
    return df_result

def main():
    
    # set parser
    parser = argparse.ArgumentParser(description='''
    Get master dates from prm files convert them to days and insert the master line (the first) in final csv file
    Input cvs file:
    lat | lon | vel | export_1 | export_2 | ....
    val | val | val | val      | val      | ....
    val | val | val | val      | val      | ....
    ...
    
    val stands for some value
    
    Outputs csv file:
    lat | lon | vel | export_1 | export_2 | ....
    0   | 0   | NAN | 1001     | 1002     | ....
                       |           |
                       +-----------+--> these are the dates in days 
                       
    Example input:
    put_dates_into_final_csv -prm path/to/prm_folder -csv path/to/final.csv''')
    
    # set arguments
    parser.add_argument('-prm', '--prm_path', metavar='', required=True, help='insert valid path for PRM files')
    parser.add_argument('-csv', '--csv_file', metavar='', required=True, help='insert valid path for csv file')
    args = parser.parse_args()

    ids_and_dates_dic = {}
    
    # search all PRM files to get dates and IDs returning a dictionary
    ids_and_dates_dic = searchFiles(args.prm_path) 
    
    # create new row for final csv
    new_row = ['0', '0', 'NaN']
    for date_in_days in ids_and_dates_dic.values():
        new_row.append(date_in_days)
        
    # insert row with dates
    df = pd.read_csv(args.csv_file)
    df = Insert_row_(0, df, new_row)
    df.to_csv(args.csv_file)
    
if __name__ == "__main__":
    main()
    