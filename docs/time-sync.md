# Time synchronization

This is performed using [Chrony](https://github.com/mlichvar/chrony). A Chrony instance is ran inside its own Docker container, ideally in the same host and Docker network as pladmed-backend, using it as a client for adjusting the server's clock. Since a Chrony instance can act both as an NTP client and NTP server, it does so, acting as an NTP server to the probes, improving the system scalability and reducing the load on public NTP servers. Visually:

![NTP architecture](docs/time-sync.png)

Assuming there's a public NTP server in the p stratum, then a pladmed-backend instance which sync with it will be in stratum (p+1). Since the same Chrony instance will act as an NTP server for the probes, all of them will be in stratum p+2. This is fine because probes measure relative times: clock drift doesn't affect them critically.