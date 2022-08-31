In this branch the changes from the main branch, made by Eurico-98, are in the automation.sh file in the last line 449:

# call python script to get dates from prm files convert them to days and insert them in final.csv
docker run -it -v $scripts_folder/post_processing/put_dates_into_final_csv:/processing_folder --rm put_dates_into_final_csv -prm $processing_folder/$orb/F$SS/raw -csv $processing_folder/$orb/SBAS/final.csv
Moreover the srcipt used here is in the location:

GMTSAR_SBAS_AUTOMATION/post_processing/put_dates_into_final_csv/

What the script does is:

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