#!/bin/sh

if [ "$DATABASE" = "mongo" ]
then
    echo "Waiting for Mongo to start on ${MONGO_HOST}:${MONGO_PORT}"

    while ! nc -z $MONGO_HOST $MONGO_PORT; do
      sleep 0.1
    done

    echo "Mongo started\n"
fi

exec "$@"
