import socket
import threading
import select
import os


class Server(object):

    addr_conn_thread = []
    bound = False
    storage_folder = os.getcwd()+"\\storage"

    def __init__(self, host, port, n=1):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.set_listen(n)
        self.bound = True
        self.open_storage_folder()

    def my_bind(self, host, port):
        self.sock.close()
        self.sock.bind((host, port))
        self.bound = True

    def close_server(self):
        self.sock.close()
        self.bound = False

    def set_listen(self, n):
        self.sock.listen(n)

    def wait_for_connection(self):
        print("Server on")
        print("Server Waiting for connection...")
        while self.bound:
            print("Waiting for connection")
            conn, addr = self.sock.accept()
            print("Connection from " + str(addr))

            new_thread = threading.Thread(target=self.send_receive,
                                          name=addr,
                                          args=[conn, addr, self.store_data, self.get_data, self.send_stored_files])
            self.addr_conn_thread.append((conn, addr, new_thread))
            new_thread.start()
            print("Thread started")

    @staticmethod
    def send_receive(conn, addr, store_data, get_data, send_stored_files):
        while 1:
            print("Waiting for request...")
            request = conn.recv(265)
            request = request.decode("utf-8")
            if request == 'q':
                print("Closing connection with" + str(addr))
                conn.close()
                return
            elif request == 's':
                print("Send")
                Server.receive_file(conn, store_data)
            elif request == 'r':
                Server.send_file(conn, addr, get_data)
                print("Receive")
            elif request == 'f':
                send_stored_files(conn, addr)

    @staticmethod
    def send_file(conn, addr, get_data):
        # Receive file name
        file_name = conn.recv(8192).decode("utf-8")

        # send file length
        file_len = os.stat(file_name).st_size
        conn.send(str(file_len).encode("utf-8"))

        # File data generator
        gen = get_data(file_name, 8192)

        # send file data
        bytes_sent = 0
        while bytes_sent < file_len:
            n_bytes = conn.send(next(gen))
            if not n_bytes:
                print("Couldn't send all data to " + str(addr))
                return
            bytes_sent += n_bytes

        print("Successfully sent all data")

    @staticmethod
    def receive_file(conn, store_data):
        # Get Message length
        msg_len = conn.recv(512)
        # Decode Message length
        msg_len = int(msg_len.decode("utf-8"))
        print("Got msg_len " + str(msg_len))

        # Get filename
        filename = conn.recv(8192)
        # Decode file extension
        filename = filename.decode("utf-8")
        print("Got filename " + filename)

        # Create loop to get all data
        total_recv = 0
        chunks = []
        while msg_len > total_recv:
            chunk = conn.recv(8192)
            if not chunk:
                raise RuntimeError("Connection was timed out from client")
            print("Receive chunk")
            chunks.append(chunk)
            total_recv += len(chunk)

        # exit thread and send data to server for storage
        print("Received all data")
        store_data(filename, b''.join(chunks))

    def get_data(self, file_name, bytes):
        self.open_storage_folder()
        f = open(file_name, 'rb')
        yield f.read(bytes)
        f.close()

    def send_stored_files(self, conn, addr):
        print("Trying to send file names to " + str(addr))
        # Get all files stored in folder
        files = [f for f in os.listdir(self.storage_folder) if os.path.isfile(f)]
        # Encode all files
        encoded_files = [f.encode("utf-8") for f in files]
        # join all files with ,
        file_str = b','.join(encoded_files)
        # Get Message Length
        total_bytes = len(file_str)

        # Send message length
        conn.send(str(total_bytes).encode("utf-8"))

        # Send message
        bytes_sent = 0
        while bytes_sent < total_bytes:
            n_bytes = conn.send(file_str[bytes_sent:])
            if n_bytes == 0:
                print("Failed to send all files in storage\nOnly sent " + str(bytes_sent) + '/' + str(total_bytes))
                conn.close()
                return
            bytes_sent += n_bytes

        print("Successfully sent stored file names to " + str(addr))

    def store_data(self, file_name, bytes_data):
        with open(file_name, 'w') as f:
            f.write(bytes_data.decode("utf-8"))
        print("Stored data")

    def open_storage_folder(self):
        if not os.path.exists(self.storage_folder):
            os.mkdir(self.storage_folder)
        os.chdir(self.storage_folder)

s = Server("192.168.1.11", 5000)
s.wait_for_connection()
