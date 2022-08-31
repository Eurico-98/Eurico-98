In this branch the changes from the main branch, made by Eurico-98, are the srcipt in the location:

GMTSAR_SBAS_AUTOMATION/post_processing/get_reference_point/

What the script does is:

Get the reference point with options:

    Option 1:
        Get ref point nearest to fixed point - example input:
        get_reference_point -op 1 -lat 45 -lon 56 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------
    Option 2:
        Get ref point from rectangular area using two points - example input:
        get_reference_point -op 2 -lat 45 -lon 56 -lat2 69 -lon2 420 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------
    Option 3:
        Get ref point from circular area using fixed point and radius - example input:
        get_reference_point -op 3 -lat 45 -lon 56 -dist 100 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------
    Option 4:
        Automatically select ref point from points with lowest standard deviation - example input:
        get_reference_point -op 4 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------
    Option 5:
        Get ref point based on median of all points - example input:
        get_reference_point -op 5 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------
    Option 6:
        Get ref point based on lowest average velocity - example input:
        get_reference_point -op 6 -csvFile (...)/final.csv
        
        Outputs a file named final_corrected.csv in the same location of the script
    ----------------------------------------------------------------------------------------------------