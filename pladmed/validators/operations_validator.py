from pladmed.validators.command_validator import (
    AnyValidator,
    BetweenValidator,
    MultiValueValidator,
    EmptyValidator,
    EmptyListValidator
)

TRACEROUTE_PARAMS = {
    "confidence": BetweenValidator(0, 0.99),
    "method": MultiValueValidator(["udp-paris", "icmp-paris", "icp"]),
    "dport": AnyValidator(),
    "firsthop": AnyValidator(),
    "maxttl": BetweenValidator(1, 255),
    "attempts": BetweenValidator(1, 10),
    "sport": AnyValidator(),
    "wait": BetweenValidator(1, 20),
    "wait-probe": BetweenValidator(0, 100)
}

PING_PARAMS = {
    "probecount": BetweenValidator(1, 100),
    "icmp-sum": AnyValidator(),
    "dport": AnyValidator(),
    "sport": AnyValidator(),
    "wait": BetweenValidator(1, 20),
    "method": MultiValueValidator(["icmp-echo", "icmp-time", "tcp-syn", "tcp-ack", "tcp-ack-sport", "udp", "udp-dport"]),
    "size": BetweenValidator(1, 255),
    "timeout": BetweenValidator(0, 100)
}

DNS_PARAMS = {
    "address": AnyValidator(),
    "ipv4": EmptyValidator(),
    "ipv6": EmptyValidator(),
    "name": AnyValidator(),
    "type": MultiValueValidator([
        "a", "any", "axfr", "hinfo", "mx", "ns", "soa", "txt"
    ]),
    "fqdns": AnyValidator(),
    "ips": EmptyListValidator()
}

GENERAL_PARAMS = {
    "ips": AnyValidator(),
    "fqdns": AnyValidator()
}
