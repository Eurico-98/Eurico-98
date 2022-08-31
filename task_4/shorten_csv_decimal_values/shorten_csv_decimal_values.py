import argparse
import pandas as pd

def correct_decimal_places(csvFile):

    # get coords of points from data frame
    df = pd.read_csv(csvFile)
    
    # first remove decimal places in values of the first line
    df.iloc[0, 3:] = df.iloc[0, 3:].apply(lambda x: format(int(x)))
    
    for column in range(len(df.columns)-1):
        
        # reduce dates to 3 decimal values
        if(column > 1 and column != 3):
            df.iloc[1:, column] = df.iloc[1:, column].apply(lambda x: format(float(x),".2f"))
    
    # write changes to csv file
    df.to_csv(csvFile,index=False,na_rep="NaN")


if __name__ == "__main__":
    
    # set parser
    parser = argparse.ArgumentParser(description='''
    Shorten decimal points.
    
    First converts values of first line after the NaN to integers, in positions -> [0, 3:]
    
    Than reduces all decimal points of the date values to 3, so in positions -> [1:, 2:]
    
    Example input:
    shorten_csv_decimal_values -csvFile (...)/final.csv

    Outputs the same file that was passed has input but correted
    ''', formatter_class=argparse.RawTextHelpFormatter)
    
    # for all options
    parser.add_argument('-csvFile', '--csvFile', metavar='', required=False, help='insert valid path to final.csv file')
    args = parser.parse_args()
   
        
    if(args.csvFile is None): 
        print("Please insert a valid path for csv file")
    else:
        correct_decimal_places(args.csvFile)