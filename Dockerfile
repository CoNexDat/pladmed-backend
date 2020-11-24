FROM python:3.6.9

ENV HOME=/home
WORKDIR $HOME

RUN apt-get update \
    && apt-get install -y netcat

COPY ./requirements.txt .
COPY ./docker-entrypoint.sh .
COPY ./main.py .

RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash"]
