import socket
import sys


def Main():
    pass


class Connection(object):

    s = socket.socket()

    def __init__(self):
        pass


    def connect(self, host, port):
        # try to connect to host
        try:
            self.s.connect((host, port))
        except TimeoutError as err:
            print("Couldn't connect to host, error code:" + err.args[0] + " - " + err.args[1])
            return "Couldn't connect to host"
        except ConnectionRefusedError as err:
            print("Host refused connection:" + err.args[0] + " - " + err.args[1])
            return "Host refused connection"
        return "Successfully Connected"

    def disconnect(self):
        self.s.close()

    def change_socket_type(self, family=socket.AF_INET, s_type=socket.SOCK_STREAM):
        # try to create socket
        try:
            self.s = socket.socket(family, s_type)
        except socket.error as err:
            print("Failed to create socket, error code: " + str(err.args[0]) + " - " + str(err.args[1]))
        except TypeError as err:
            print("Host or port incorrect type, error code: " + str(err.args[0]) + " - " + str(err.args[1]))

if __name__ == "__main__":
    Main()
