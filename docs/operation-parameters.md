# Operation parameters

This section defines which parameters can be sent to each kind of operation, and their type and allowed values, if applicable.

For details on the meaning of each parameter, refer to [Scamper manual](https://www.caida.org/tools/measurement/scamper/man/scamper.1.pdf).

All ranges include the edge values.

## General parameters

These three parameters are mandatory for any kind of operation.

* **cron**: A cron expression which defines the frequency to use for running the operation. Since cron doesn't handle years, an operation cannot run for longer than a year. It is recommended to use [Cron Guru](https://crontab.guru/) for validating this value beforehand.

* **stop_time**: A date and time defining when the measurement operation should end. It is expected to be in `dd/mm/YYYY HH:MM` format (the single space between date and time is expected and mandatory).

* **times_per_minute**: Since cron doesn't allow resolution beyond minutes, this setting allows for that smaller granularity. One second is the limit, so this value must be an integer between 1 and 60.

## Operation-specific parameters

### traceroute

* **attempts**: An integer number between 1 and 10.

* **confidence**: Floating point number between 0 and 0.99.

* **dport**: An integer greater than zero.

* **fqdns**: A comma-separated list of strings. If `ips` is empty, must be present.

* **firsthop**: An integer greater than zero.

* **ips**: A comma-separated list of IPv4 or IPv6 addresses. If `fqdns` is empty, must be present.

* **maxttl**: An integer between 1 and 255.

* **method**: A string. Can only be "icmp-paris", "icp" or "udp-paris".

* **sport**: An integer greater than zero.

* **wait**: An integer between 1 and 20.

* **wait-probe**: An integer between 0 and 100.

### ping

* **dport**: An integer greater than zero.

* **fqdns**: Same as name: a comma-separated list of strings. If `ips` is empty, must be present.

* **icmp-sum**: An integer greater than zero.

* **ips**: A comma-separated list of IPv4 or IPv6 addresses. If `fqdns` is empty, must be present.

* **method**: A string. Can only be "icmp-echo", "icmp-time", "tcp-ack", "tcp-ack-sport", "tcp-syn", "udp", or "udp-dport".

* **probecount**: An integer between 1 and 100.

* **size**: An integer between 1 and 255.

* **sport**: An integer greater than zero.

* **timeout**: An integer between 0 and 100.

* **wait**: An integer between 1 and 20.

### dns

* **address**: A string representing an IPv4 or IPv6 address.

* **fqdns**: Same as name: a comma-separated list of strings.

* **ips**: Will error if not empty. This is mainly to avoid confusion. Use -x for reverse lookup.

* **ipv4**: This is a switch, so no value should be provided. Actually, if a value is provided, it will be considered an error.

* **ipv6**: This is a switch, so no value should be provided. Actually, if a value is provided, it will be considered an error.

* **name**: A comma-separated list of strings.

* **type**: A string. Can only be "a", "any", "axfr", "hinfo", "mx", "ns", "soa", or "txt".

* **x**: A string representing an IPv4 or IPv6 address on which to perform reverse lookup.
