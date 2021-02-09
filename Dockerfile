# Stage 0: server
FROM python:3.6.9 AS server

ENV HOME=/home
WORKDIR $HOME

RUN apt-get update \
    && apt-get install -y netcat

COPY ./requirements.txt .
COPY ./docker-entrypoint.sh .
COPY ./main.py .

RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash"]

# Stage 1: chrony
FROM geoffh1977/chrony:latest AS chrony

# Uncomment to use custom config. The Docker file's
# automated settings seemed good enough on preliminary testing
# COPY time-sync/chrony.conf /etc/chrony.conf