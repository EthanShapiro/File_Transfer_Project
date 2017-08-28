import socket
import sys


def Main():
    pass


class Connection(object):

    def __init__(self):
        self.change_socket_type()
        self.connected = False

    def connect(self, host, port):
        # try to connect to host
        try:
            self.sock.connect((host, port))
        except TimeoutError as err:
            print("Couldn't connect to host, error code:" + err.args[0] + " - " + err.args[1])
            return "Couldn't connect to host"
        except ConnectionRefusedError as err:
            print("Host refused connection:" + err.args[0] + " - " + err.args[1])
            return "Host refused connection"
        self.connected = True
        return "Successfully Connected"

    def disconnect(self):
        self.connected = False
        self.sock.close()

    def change_socket_type(self, family=socket.AF_INET, s_type=socket.SOCK_STREAM):
        # try to create socket
        try:
            self.sock = socket.socket(family, s_type)
        except socket.error as err:
            print("Failed to create socket, error code: " + str(err.args[0]) + " - " + str(err.args[1]))
        except TypeError as err:
            print("Host or port incorrect type, error code: " + str(err.args[0]) + " - " + str(err.args[1]))

    def my_send(self, data):
        """
        Send bytes to host if connected
        :param data:
        :return:
        """
        # TODO Implement flags 'learn what flags are'
        if not self.connected:
            return
        if type(data) is not bytes:
            return
        total_sent = 0
        data_len = len(data)
        while total_sent < data_len:
            n_sent = self.sock.send(data[total_sent:])
            if n_sent:
                raise RuntimeError("socket connection broken")
            total_sent += n_sent

    def my_recieve(self):
        chunks = []

    def get_msg_len(self):
        data = self.sock.recv(512)
        return int.from_bytes(data, 'big')


if __name__ == "__main__":
    Main()
