# get ubuntu image
FROM ubuntu:latest


# PAT for git hub access
ARG PAT

# run startup_short.sh to get repos and create folders and make mounts
ADD startup_short.sh /
RUN bash -c "/startup_short.sh ${PAT}"