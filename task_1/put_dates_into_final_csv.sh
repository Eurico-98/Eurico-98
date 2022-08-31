#!/bin/bash 

# call python script to get dates from prm files convert them to days and insert them in final.csv
python3 put_dates_into_final_csv/put_dates_into_final_csv.py -prm $processing_folder/$orb/F$SS/raw -csv $processing_folder/$orb/SBAS/final.csv
