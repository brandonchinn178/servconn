import socket, json

class SocketConnector:
    def __init__(self, host, port, bufsize=4096):
        """
        Initializes a socket connection with the provided server.

        @param host -- the host to connect to
        @param port -- the port to connect to
        @param bufsize -- the size of data allowed to be received (default 4096)
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (host, port)
        self.bufsize = bufsize

    def send(self, data):
        """
        Sends the data to the server as a JSON string and returns the response.

        @param data -- a Python object to send as JSON

        @return (object) the response from the server as a Python object extracted from
            the JSON formatted string
        """
        self.socket.connect(self.address)
        self.socket.send(json.dumps(data))
        response = self.socket.recv(self.bufsize)
        self.socket.close()
        return json.loads(response)