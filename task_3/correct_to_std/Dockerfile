FROM python:3

WORKDIR /app

ADD correct_to_std.py .

RUN pip3 install pandas \
    rtree

ENTRYPOINT ["python3", "correct_to_std.py"]