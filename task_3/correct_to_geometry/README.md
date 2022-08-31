In this branch the changes from the main branch, made by Eurico-98, are the srcipt in the location:

GMTSAR_SBAS_AUTOMATION/post_processing/point_correction_tools/

What the script does is:

Get the reference point with options:

    Option 1:
        Get ref point nearest to fixed point - example input:
        correct_to_geometry -op 1 -lat 45 -lon 56 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------
    Option 2:
        Get ref point from rectangular area using two points - example input:
        correct_to_geometry -op 2 -lat 45 -lon 56 -lat2 69 -lon2 420 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------
    Option 3:
        Get ref point from circular area using fixed point and radius - example input:
        correct_to_geometry -op 3 -lat 45 -lon 56 -dist 100 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------