FROM python:3

WORKDIR /app

ADD put_dates_into_final_csv.py .

RUN python3 pip install pandas \
    rtree

ENTRYPOINT ["python3.11", "put_dates_into_final_csv.py"]