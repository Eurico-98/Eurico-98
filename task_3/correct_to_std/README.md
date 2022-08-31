In this branch the changes from the main branch, made by Eurico-98, are the srcipt in the location:

GMTSAR_SBAS_AUTOMATION/post_processing/point_correction_tools/

What the script does is:

Get the reference point using standart deviation:

    Automatically select ref point from points with lowest standard deviation - example input:
    correct_to_std -csvFile (...)/final.csv
    
    Outputs a file named final_corrected.csv in the same location of the script