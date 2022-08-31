In this branch the changes from the main branch, made by Eurico-98, are the srcipt in the location:

GMTSAR_SBAS_AUTOMATION/post_processing/

What the script does is:

Reduces deimal points of date values to rteduce the size of csv file

    Shorten decimal points.
    
    First converts values of first line after the NaN to integers, in positions -> [0, 3:]
    
    Than reduces all decimal points of the date values to 3, so in positions -> [1:, 2:]
    
    Example input:
    shorten_csv_decimal_values -csvFile (...)/final.csv

    Outputs the same file that was passed has input but correted