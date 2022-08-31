FROM python:3

WORKDIR /

ADD divide_data_files.py .

RUN pip3 install rtree

COPY commands.sh ./commands.sh

RUN ["chmod", "+x", "./commands.sh"]

ENTRYPOINT ["./commands.sh"]