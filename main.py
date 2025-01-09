import socket
import threading

class UDPProxyServer:
    def __init__(self, host, port, remote_host, remote_port):
        self.host = host
        self.port = port
        self.remote_host = remote_host
        self.remote_port = remote_port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))

    def handle_client(self, client_address, data):
        try:
            # Send data to remote server
            self.server_socket.sendto(data, (self.remote_host, self.remote_port))

            # Receive response from remote server
            response, _ = self.server_socket.recvfrom(1024)

            # Send response back to client
            self.server_socket.sendto(response, client_address)

        except Exception as e:
            print(f"Error handling client: {e}")

    def start(self):
        print(f"UDP Proxy Server started on {self.host}:{self.port}")

        while True:
            try:
                data, client_address = self.server_socket.recvfrom(1024)
                thread = threading.Thread(target=self.handle_client, args=(client_address, data))
                thread.start()

            except Exception as e:
                print(f"Error receiving data: {e}")

if __name__ == "__main__":
    # Example usage
    host = 'localhost'  # Localhost for this example
    port = 5000
    remote_host = '174.138.123.212'  # Replace with actual remote host IP
    remote_port = 5001

    proxy_server = UDPProxyServer(host, port, remote_host, remote_port)
    proxy_server.start()