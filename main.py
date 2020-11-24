# !/usr/local/bin/python

from pladmed import create_app, socketio
import os

app = create_app()

def start_server():
    port = int(os.getenv('PORT', 5000))
    debug = int(os.getenv('DEBUG', True))
    host = os.getenv("HOST", "0.0.0.0")

    socketio.run(app, port=port, host=host, debug=debug)

if __name__ == '__main__':
    start_server()
