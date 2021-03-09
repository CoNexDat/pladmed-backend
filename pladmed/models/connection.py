class Connection:
    def __init__(self, sid, total_credits, in_use_credits):
        self.sid = sid
        self.total_credits = total_credits
        self.in_use_credits = in_use_credits
