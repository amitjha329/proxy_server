import socket
import threading
from http.server import BaseHTTPRequestHandler

class HTTPProxyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_request_to_remote_server('GET')

    def do_POST(self):
        self.send_request_to_remote_server('POST')

    def send_request_to_remote_server(self, method):
        try:
            # Create a socket to connect to the remote server
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((self.headers['Host'].split(':')[0], 80)) 

            # Construct the request to send to the remote server
            request_headers = f"{method} {self.path} HTTP/1.1\r\n"
            request_headers += f"Host: {self.headers['Host']}\r\n"
            request_headers += f"Connection: close\r\n"  # Close connection after request
            for header in self.headers:
                if header not in ('Host', 'Connection'):
                    request_headers += f"{header}: {self.headers[header]}\r\n"
            request_headers += "\r\n"

            if method == 'POST':
                request_headers += self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')

            # Send the request to the remote server
            remote_socket.sendall(request_headers.encode('utf-8'))

            # Receive the response from the remote server
            response = b''
            while True:
                chunk = remote_socket.recv(4096)
                if not chunk:
                    break
                response += chunk

            remote_socket.close()

            # Send the response to the client
            self.send_response(200) 
            for line in response.decode('utf-8').split('\r\n'):
                if line:
                    self.send_header(line.split(':')[0].strip(), line.split(':')[1].strip())
            self.end_headers()
            self.wfile.write(response)

        except Exception as e:
            print(f"Error handling request: {e}")
            self.send_error(500, "Internal Server Error")

class HTTPProxyServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        from http.server import HTTPServer
        server = HTTPServer((self.host, self.port), HTTPProxyRequestHandler)
        print(f"HTTP Proxy Server started on {self.host}:{self.port}")
        server.serve_forever()

if __name__ == "__main__":
    # Example usage
    host = '139.59.20.219'
    port = 8080

    proxy_server = HTTPProxyServer(host, port)
    proxy_server.start()