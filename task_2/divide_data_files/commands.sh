#!/bin/bash

mv divide_data_files.py raw/

cd raw/

python3 divide_data_files.py -ncpus $1 -data_in $2 -subswaths $3