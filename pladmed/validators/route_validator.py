from pladmed.validators.operations_validator import TRACEROUTE_PARAMS, PING_PARAMS, DNS_PARAMS
from pladmed.validators.command_validator import InvalidParam


def validate_params(data, valid_params):
    try:
        for param in data:
            if param in valid_params:
                validator = valid_params[param]
                validator.validate(data[param])
        return True
    except InvalidParam:
        return False


def validate_probes(data):
    return len(data["probes"]) > 0


def validate_destinations(data):
    if "fqdns" not in data or "ips" not in data:
        return False
    total_destinations = 0
    if "fqdns" in data:
        total_destinations += len(data["fqdns"])
    if "ips" in data:
        total_destinations += len(data["ips"])
    return total_destinations != 0


def validate_traceroute(data):
    if "probes" not in data or "params" not in data:
        return False
    return validate_probes(data["probes"]) and validate_params(data["params"], TRACEROUTE_PARAMS) and \
        validate_destinations(data["params"])


def validate_ping(data):
    if "probes" not in data or "params" not in data:
        return False
    return validate_probes(data["probes"]) and validate_params(data["params"], PING_PARAMS) and validate_destinations(
        data["params"])


def validate_dns(data):
    if "probes" not in data or "params" not in data:
        return False
    return validate_probes(data["probes"]) and validate_params(data["params"], DNS_PARAMS) and validate_destinations(
        data["params"])
