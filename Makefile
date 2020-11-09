SHELL := /bin/bash
PWD := $(shell pwd)

all:

start:
	FLASK_APP=src/main.py flask run --host 0.0.0.0
.PHONY: start

debug:
	FLASK_APP=src/main.py FLASK_ENV=development flask run --host 0.0.0.0
.PHONY: debug