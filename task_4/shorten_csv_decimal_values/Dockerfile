FROM python:3

WORKDIR /app

ADD shorten_csv_decimal_values.py .

RUN pip3 install pandas \
    rtree

ENTRYPOINT ["python3", "shorten_csv_decimal_values.py"]