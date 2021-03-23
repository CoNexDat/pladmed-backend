SHELL := /bin/bash
PWD := $(shell pwd)

all:

build:
	docker build -f ./Dockerfile --target server -t "server:latest" .
	docker build -f ./time-sync/Dockerfile --target chrony -t "chrony" .
.PHONY: build

start: build
	docker-compose up -d
.PHONY: start

logs:
	docker-compose logs -f
.PHONY: logs

stop:
	docker-compose stop -t 1
	docker-compose down
.PHONY: stop

debug: build
	docker-compose up -d
	docker-compose logs -f
.PHONY: debug

test: build
	-COMPOSE_PROJECT_NAME=testing \
	GREEN="\033[32m" \
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-test.yaml up \
	--abort-on-container-exit
	COMPOSE_PROJECT_NAME=testing \
	docker cp pladmed-testing:/home/coverage.xml .coverage
	docker-compose -p COMPOSE_PROJECT_NAME -f docker-compose-test.yaml down
.PHONY: test
