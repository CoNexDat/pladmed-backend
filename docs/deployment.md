# Deployment

## A possible deployment strategy

![Deployment diagram](docs/deployment-diagram.png)

This diagram depicts the recommended deployment strategy for the system as a whole.

Firstly, pladmed-frontend can be served via any web server (Apache2, nginx) so users can access it in their own browser across the Internet. On the other hand, those same users, or different ones, can run their own probes by installing them in their system (see [the probe documentation](https://github.com/fedefunes96/pladmed-client)) for details.

Secondly, each server will have three docker containers:

1. server: Runs a pladmed-backend instance, including a web server which will listen for HTTP requests from the frontend, and web socket connections from probes.
2. db: Runs a MongoDB database instance for persisting users, operations and their results.
3. chrony: Runs a Chrony client/server. Acts as an NTP client for pladmed-backend, and as an NTP server for probes.

## pladmed-backend installation in a server environment

TODO