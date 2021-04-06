# Operation parameters

This section defines which parameters can be sent to each kind of operation, and their type and allowed values, if applicable.

For details on the meaning of each parameter, refer to [Scamper manual](https://www.caida.org/tools/measurement/scamper/man/scamper.1.pdf).

All ranges include the edge values.

## traceroute

* **attempts**: An integer number between 1 and 10.

* **confidence**: Floating point number between 0 and 0.99.

* **dport**: An integer greater than zero.

* **firsthop**: An integer greater than zero.

* **maxttl**: An integer between 1 and 255.

* **method**: A string. Can only be "icmp-paris", "icp" or "udp-paris".

* **sport**: An integer greater than zero.

* **wait**: An integer between 1 and 20.

* **wait-probe**: An integer between 0 and 100.

## ping

* **dport**: An integer greater than zero.

* **icmp-sum**: An integer greater than zero.

* **method**: A string. Can only be "icmp-echo", "icmp-time", "tcp-ack", "tcp-ack-sport", "tcp-syn", "udp", or "udp-dport".

* **probecount**: An integer between 1 and 100.

* **size**: An integer between 1 and 255.

* **sport**: An integer greater than zero.

* **timeout**: An integer between 0 and 100.

* **wait**: An integer between 1 and 20.

## dns

* **address**: A string representing an IPv4 or IPv6 address.

* **fqdns**: Same as name: a comma-separated list of strings.

* **ips**: Will error if not empty. This is mainly to avoid confusion. Use -x for reverse lookup.

* **ipv4**: This is a switch, so no value should be provided. Actually, if a value is provided, it will be considered an error.

* **ipv6**: This is a switch, so no value should be provided. Actually, if a value is provided, it will be considered an error.

* **name**: A comma-separated list of strings.

* **type**: A string. Can only be "a", "any", "axfr", "hinfo", "mx", "ns", "soa", or "txt".

* **x**: A string representing an IPv4 or IPv6 address on which to perform reverse lookup.
