import argparse
import pandas as pd
pd.options.mode.chained_assignment = None

def correct_csv_to_std(csvFile):
    
    df = pd.read_csv(csvFile)
    
    min_std = 0
    line_index = 0
    aux = 0
    
    for i in df.index:
        
        # initialize min_std
        if(i == 1):
            min_std = df.iloc[i, 3:].std()
            line_index = i
        
        elif(i > 1):
            aux = df.iloc[i, 3:].std()
            if(aux < min_std):
                min_std = aux
                line_index = i
        
    # in case input file only has header and master line there will be no other values to subtract
    if(line_index > 0):         
        
        # first correct average velocity column
        df.iloc[1:,2] = df.iloc[1:,2] - df.iloc[line_index,2]
        
        # get first line from original csv file
        first_line = df.iloc[0, :]
        
        # put coordinates of reference point in first line
        first_line.iloc[0:2] = df.iloc[line_index, 0:2]
        
        # put first line in final corrected csv file
        df.iloc[0, :] = first_line
         
        df_points = df.iloc[1:, 3:]
        
        # ajust index of line with the reference point -> remove one representing the first line
        line_index -= 1
        
        for col_index in range(len(df_points.columns)-1):
            df_points.iloc[:, col_index] = df_points.iloc[:, col_index] - df_points.iloc[line_index, col_index]
        
        df.iloc[1:, 3:] = df_points
        
    # create new file
    newFinalCsv = create_final_corrected_csv(csvFile)
    
    # write changes to new file
    df.to_csv(newFinalCsv,index=False,na_rep="NaN")


def create_final_corrected_csv(csvFile):
    
    path = csvFile.split("/")
    newFinalCsv = ''
    
    for file in path:
        if(len(file.split(".")) == 2 and file.split(".")[1] == "csv"):
            newFinalCsv += file.split(".")[0] + "_corrected.csv"
    
    f = open(newFinalCsv, 'w')
    f.close()
    
    return newFinalCsv


if __name__ == "__main__":
    
    # set parser
    parser = argparse.ArgumentParser(description='''
    
    Automatically select ref point from points with lowest standard deviation - example input:
    correct_to_std -csvFile (...)/final.csv
    
    Outputs a file named final_corrected.csv in the same location of the script
    ''', formatter_class=argparse.RawTextHelpFormatter)
    
    # for all options
    parser.add_argument('-csvFile', '--csvFile', metavar='', required=False, help='insert valid path to final.csv file')
    args = parser.parse_args()
    
        
    if(args.csvFile is None): 
        print("Please insert a valid path for csv file")
    else:
        correct_csv_to_std(args.csvFile)
    