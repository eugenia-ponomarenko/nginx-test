from flask import Flask
from flask_sock import Sock
from multiprocessing import Process

ports = [8080, 8081, 8082]
apps = {}


for port in ports:
    app = Flask(__name__)
    apps[port] = {'app': app}

def add_routes(app, port):
    @app.route('/')
    def home():
        return f"Hello from server on port {port}!"

    @app.route('/admin')
    def admin():
        return f"Admin Page on port {port}!"


# Initialize Sock for app3 (port 8082)
web_sock = Sock(apps[8082]['app'])

@web_sock.route('/ws')
def handle_message(ws):
    while True:
        text = ws.receive()
        ws.send('You send me: ' + text)


def run_app(port):
    apps[port]['app'].run(debug=True, host='0.0.0.0', port=port)


# Add routes for each app
for port, data in apps.items():
    add_routes(data['app'], port)


if __name__ == '__main__':
    processes = [Process(target=run_app, args=(port,)) for port in ports]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
