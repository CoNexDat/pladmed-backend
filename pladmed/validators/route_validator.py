from pladmed.validators.operations_validator import TRACEROUTE_PARAMS, PING_PARAMS, DNS_PARAMS
from pladmed.validators.command_validator import InvalidParam
from flanker.addresslib import address


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
    return len(data) > 0


def validate_destinations(data):
    if "fqdns" not in data and "ips" not in data:
        return False
    total_destinations = 0
    if "fqdns" in data:
        total_destinations += len(data["fqdns"])
    if "ips" in data:
        total_destinations += len(data["ips"])
    return total_destinations != 0


def validate_traceroute(data):
    return validate_operation(data, TRACEROUTE_PARAMS)


def validate_ping(data):
    return validate_operation(data, PING_PARAMS)


def validate_dns(data):
    return validate_operation(data, DNS_PARAMS)


def validate_operation(data, valid_params):
    if "probes" not in data or "params" not in data:
        return False
    return validate_probes(data["probes"]) and validate_params(data["params"], valid_params) and validate_destinations(
        data["params"])


def validate_user_data_present(data):
    if "email" not in data or data["email"] == "":
        return "Missing email field"
    if "password" not in data or data["password"] == "":
        return "Missing password field"
    addr = address.validate_address(data["email"])
    if addr == None:
        return "Email address has invalid format, or MX domain does not exist"
    return ""


def validate_user_data(data):
    validation_error = validate_user_data_present(data)
    if validation_error != "":
        return validation_error

    password = data["password"]
    special_characters = '!"@#$%^&*()-+?_=,/'
    rules = [lambda s: any(x.isupper() for x in s),  # must have at least one uppercase
             # must have at least one lowercase
             lambda s: any(x.islower() for x in s),
             lambda s: any(x.isdigit()
                           for x in s),  # must have at least one digit
             # must be at least 8 characters
             lambda s: len(s) >= 8,
             lambda s: any(x in special_characters for x in s),
             ]

    if not all(rule(password) for rule in rules):
        return "Password must have at least 8 characters, 1 uppercase character, 1 lowercase, 1 digit and 1 special character"

    return ""


def validate_credits(data):
    return "id" in data and data["id"] != "" and "credits" in data and data["credits"] > 0
