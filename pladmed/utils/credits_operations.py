CREDITS_PER_TRACEROUTE = 15
CREDITS_PER_PING = 1

def calculate_credits_traceroute(total_ips):
    return CREDITS_PER_TRACEROUTE * total_ips

def calculate_credits_ping(total_ips):
    return CREDITS_PER_PING * total_ips
