class Connection:
    def __init__(self, conn):
        self.conn = conn
        self.alive = True

    def disconnect(self):
        self.alive = False

    def __eq__(self, other):
        return self.conn == other.conn
