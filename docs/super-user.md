# Creating a super user

To grant an initial amount of credits to a standard user, a super user is required. For security reasons, creating a super user can only be done from a shell attached to the Docker container where pladmed-backend is running.

Assuming a Debian-like server environment, in a terminal, the first step is using `docker ps` to get the name of the container. This will return a list such as the following one:

```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
7bd53641f85d        mongo:3.6           "docker-entrypoint.s…"   4 minutes ago       Up 4 minutes        27017/tcp                pladmed-database
849593f8685d        chrony              "tini -- /usr/local/…"   4 minutes ago       Up 4 minutes        123/udp                  chrony
17d918db4681        server:latest       "./docker-entrypoint…"   4 minutes ago       Up 4 minutes        0.0.0.0:5000->5000/tcp   pladmed-server
```
The value which identifies the container is `CONTAINER ID`. For this pladmed-server instance, that value is `17d918db4681`. So, to attach a shell to it:

`docker exec -it 17d918db4681 bash`

Once inside the container shell, the command for creating a super user is as follows:

`flask superuser create <email> <password>`

Of course, replace `<email>` and `<password>` with the new super user credentials, without the angle brackets.

Once the super user has been created, it's possible to log in against the login endpoint with its credentials in order to obtain the super user's token. With that token, it's possible to call the `credits` endpoint, providing a user ID and the amount of credits to grant.
