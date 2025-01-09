import socket
import threading

class ProxyServer:
    def __init__(self, host='139.59.20.219', port=8080):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(100)
        print(f"Proxy server running on {host}:{port}")

    def handle_client(self, client_socket):
        request = client_socket.recv(4096)
        # Parse the request to extract the remote host and port
        request_line = request.split(b'\n')[0]
        url = request_line.split(b' ')[1]
        http_pos = url.find(b'://')
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos+3):]
        port_pos = temp.find(b':')
        webserver_pos = temp.find(b'/')
        if webserver_pos == -1:
            webserver_pos = len(temp)
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        remote_host = webserver.decode('utf-8')
        remote_port = port

        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
        remote_socket.send(request)
        response = remote_socket.recv(4096)
        client_socket.send(response)
        client_socket.close()
        remote_socket.close()

    def start(self):
        while True:
            client_socket, addr = self.server.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    proxy = ProxyServer()
    proxy.start()
