FROM python:3

WORKDIR /app

ADD correct_to_geometry.py .

RUN pip3 install pandas \
    geopandas \
    shapely \
    rtree

ENTRYPOINT ["python3", "correct_to_geometry.py"]