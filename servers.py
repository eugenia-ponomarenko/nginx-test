from flask import Flask
from flask_sock import Sock
from multiprocessing import Process

ports = [8080, 8081, 8082]
apps = {}

for port in ports:
    app = Flask(__name__)
    sock = Sock(app) if port == 8082 else None  # Only initialize Sock for app3 (port 8082)
    apps[port] = {'app': app, 'sock': sock}


def add_routes(app, port):
    @app.route('/')
    def home():
        return f"Hello from server on port {port}!"

    @app.route('/admin')
    def admin():
        return f"Admin Page on port {port}!"


def add_ws_route(sock):
    @sock.route('/ws')
    def handle_message(ws):
        while True:
            text = ws.receive()
            ws.send(f'You sent me: {text}')


def run_app(port):
    apps[port]['app'].run(debug=True, host='0.0.0.0', port=port)


# Add routes for each app
for port, data in apps.items():
    add_routes(data['app'], port)
    if data['sock']:
        add_ws_route(data['sock'])  # Add WebSocket route only for app3 (port 8082)

if __name__ == '__main__':
    processes = [Process(target=run_app, args=(port,)) for port in ports]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
