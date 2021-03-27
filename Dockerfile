FROM python:3.6.9 AS server

COPY ./scamper ./scamper

RUN apt-get install -y gcc g++ libffi-dev \
    && cd scamper && ./configure && make && make install && git

RUN ldconfig
RUN chmod -R +x scamper/

ENV HOME=/home
WORKDIR $HOME

RUN apt-get update \
    && apt-get install -y netcat

COPY ./requirements.txt .
COPY ./docker-entrypoint.sh .
COPY ./main.py .
RUN MKDIR .git
COPY .git/ .git/

RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash"]
