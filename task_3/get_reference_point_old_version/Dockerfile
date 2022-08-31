FROM python:3

WORKDIR /app

ADD get_reference_point.py .

RUN pip3 install pandas \
    geopandas \
    shapely \
    rtree

ENTRYPOINT ["python3", "get_reference_point.py"]