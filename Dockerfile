FROM python:3.6.9

ENV HOME=/home
WORKDIR $HOME

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/sh"]
