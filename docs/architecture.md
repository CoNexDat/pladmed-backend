# Architecture and robustness considerations

![Architecture diagram](architecture-diagram.png)

In this diagram, the system's architectural focus on robustness can be appreciated. For starters, there's the actors who trigger events by sending messages against an instance of pladmed-backend. On the full system, this will be done by pladmed-frontend. Each instance of pladmed-backend will use MongoDB for persisting its data, and a Chrony server/client for time synchronization.

MongoDB was chosen because it's well suited for the unstructured nature of the operation results' data. It's simple to use, which speeds up development. Reliability can be achieved by using WriteConcern, and scalability and fault tolerance with replicas.

Regarding Chrony, it can act both as a client (for adjusting the server's clock) and as a server (to provide time to the probes in a scalable way). Clock drift is not critical to pladmed, since measurements deal with time differences. So NTP is good enough in this aspect.

The servers communicate with the probes via web sockets; this simplifies communication, since objects can be sent straight away and there is no need to design an internal protocol, or middleware. For scaling up, adding more servers and a publisher/subscriber broker (Redis, Kafka, RabbitMQ) is the way to go.