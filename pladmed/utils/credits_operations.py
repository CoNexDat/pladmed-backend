from croniter import croniter
from datetime import datetime

CREDITS_PER_TRACEROUTE = 15
CREDITS_PER_PING = 1
CREDITS_PER_DNS = 1

CREDITS_PER_RESULT = 10

#TODO Credits per total Operations - use CRONTAB

def estimate_executions(cron, stop_time):
    iterat = croniter(cron)
    
    first_date = iterat.get_next(datetime)
    second_date = iterat.get_next(datetime)
    stop_date = datetime.strptime(stop_time, '%d/%m/%Y %H:%M')

    if stop_date < first_date:
        return 1

    # Executions per minute
    frequency_ex = (second_date - first_date).total_seconds()

    difference = (stop_date - first_date).total_seconds()

    executions = difference / frequency_ex

    # It'll execute once (second_date > stop_date)
    if executions < 1.0:
        return 1

    return executions

def calculate_credits_traceroute(cron, stop_time, ex_per_min, total_ips):
    executions = estimate_executions(cron, stop_time)

    credits_per_probe = CREDITS_PER_TRACEROUTE * total_ips

    return [credits_per_probe, credits_per_probe * executions * ex_per_min]

def calculate_credits_ping(cron, stop_time, ex_per_min, total_ips):
    executions = estimate_executions(cron, stop_time)

    credits_per_probe = CREDITS_PER_PING * total_ips

    return [credits_per_probe, credits_per_probe * executions * ex_per_min]

def calculate_credits_dns(cron, stop_time, ex_per_min, total_domains):
    executions = estimate_executions(cron, stop_time)

    credits_per_probe = CREDITS_PER_DNS * total_domains

    return [credits_per_probe, credits_per_probe * executions * ex_per_min]
