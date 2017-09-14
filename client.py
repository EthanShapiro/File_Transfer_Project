import socket
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QComboBox
from PyQt5.Qt import Qt, QRegExp, QRegExpValidator, QIcon
from PyQt5.QtGui import QFont
import threading
import pdb
import sys


class Gui(QWidget):

    font = QFont("Times New Roman", 13)
    connecting = False

    def __init__(self):
        super().__init__()
        self.c = Client()

        self.setWindowTitle("File to Server Transfer")
        self.initGui()
        self.setMinimumWidth(850)
        self.setMaximumWidth(850)

        self.setMinimumHeight(220)
        self.setMaximumHeight(220)

        self.show()

    def connect_to_addr_gui(self):
        # Create main connect layout
        layout = QGridLayout()

        # Add host and port labels to layout
        host_label = QLabel("Host:")
        host_label.setFont(self.font)
        layout.addWidget(host_label, 0, 0)
        port_label = QLabel("Port:")
        port_label.setFont(self.font)
        layout.addWidget(port_label, 0, 1)

        # Add host and port inputs
        ipv4_input = ipLineEdit()
        layout.addWidget(ipv4_input, 1, 0, Qt.AlignRight)
        port_input = QLineEdit()
        port_input.setFont(self.font)
        port_input.setMinimumWidth(55)
        port_input.setMaximumWidth(55)
        layout.addWidget(port_input, 1, 1)

        # Add Connect Button
        conn_btn = QPushButton("Connect")
        conn_btn.setFont(self.font)
        conn_btn.setMinimumWidth(150)
        conn_btn.setMaximumWidth(150)
        layout.addWidget(conn_btn, 2, 0)

        # Add Disconnect Button
        disconn_btn = QPushButton("Disconnect")
        disconn_btn.setFont(self.font)
        disconn_btn.setMinimumWidth(150)
        disconn_btn.setMaximumWidth(150)
        layout.addWidget(disconn_btn, 2, 1)

        # Add Connected Label
        conn_label = QLabel("Disconnected")
        conn_label.setFont(self.font)
        conn_label.setObjectName('conn_label')
        conn_label.setStyleSheet('QLabel#conn_label {color: red}')
        layout.addWidget(conn_label, 3, 0)

        # Add Connection Details
        conn_details = QLabel("No Connection Details.")
        conn_details.setFont(self.font)
        layout.addWidget(conn_details, 4, 0, 5, 2)

        # Set column stretch
        layout.setColumnStretch(0, 3)
        layout.setRowStretch(4, 7)

        # Add connection layout to main layout
        self.main_layout.addLayout(layout)

        return ipv4_input, port_input, conn_btn, disconn_btn, conn_label, conn_details

    def send_recv_gui(self):
        # Create main send and receive layout
        layout = QGridLayout()

        # Add send label
        send_label = QLabel("Send:")
        send_label.setFont(self.font)
        layout.addWidget(send_label, 0, 0)

        # Add send file path input
        send_input = QLineEdit()
        send_input.setFont(self.font)
        send_input.setMinimumWidth(450)
        send_input.setMaximumWidth(450)
        layout.addWidget(send_input, 1, 0)

        # Add file dialog
        file_dialog = QPushButton("...")
        file_dialog.setFont(self.font)
        file_dialog.setMinimumWidth(25)
        file_dialog.setMaximumWidth(25)
        layout.addWidget(file_dialog, 1, 1)

        # Add send button
        send_btn = QPushButton("Send")
        send_btn.setFont(self.font)
        send_btn.setMinimumWidth(450)
        send_btn.setMaximumWidth(450)
        layout.addWidget(send_btn, 2, 0)

        # Add Receive file input
        recv_label = QLabel("Receive:")
        recv_label.setFont(self.font)
        layout.addWidget(recv_label, 3, 0)

        # Add Receive file input
        file_select = QComboBox()
        file_select.setMinimumWidth(450)
        file_select.setMaximumWidth(450)
        file_select.setFont(self.font)
        layout.addWidget(file_select, 4, 0)

        # Add refresh files button
        refresh_btn = QPushButton()
        refresh_btn.setIcon(QIcon("refresh_icon.png"))
        refresh_btn.setMaximumWidth(25)
        refresh_btn.setMaximumHeight(25)
        layout.addWidget(refresh_btn, 4, 1)

        # Add Receive button
        recv_btn = QPushButton("Receive")
        recv_btn.setFont(self.font)
        recv_btn.setMinimumWidth(450)
        recv_btn.setMaximumWidth(450)
        layout.addWidget(recv_btn, 5, 0)

        # Add Network Details
        ntwk_details = QLabel("Currently no send/receive info")
        ntwk_details.setFont(self.font)
        layout.addWidget(ntwk_details, 6, 0, 7, 1)

        # Add Send and Receive layout to main layout
        self.main_layout.addLayout(layout)

        return send_input, send_btn, file_dialog, file_select, refresh_btn, recv_btn, ntwk_details

    def initGui(self):

        self.main_layout = QHBoxLayout()

        send_input, send_btn, file_dialog, file_select, refresh_btn, recv_btn, ntwk_details = self.send_recv_gui()

        ipv4_input, port_input, conn_btn, disconn_btn, conn_label, conn_details = self.connect_to_addr_gui()

        # Set Input Validators
        port_reg = QRegExp("\d{5}")
        port_vali = QRegExpValidator(port_reg, port_input)
        port_input.setValidator(port_vali)

        # Add Button Functions
        conn_btn.released.connect(lambda: self.connect(ipv4_input.text(), port_input.text(), conn_details, conn_label))
        disconn_btn.released.connect(lambda: self.c.disconnect(conn_label, conn_details))
        file_dialog.released.connect(lambda: self.browse(send_input))
        refresh_btn.released.connect(lambda: self.c.request_file_names(file_select))
        recv_btn.released.connect(lambda: self.c.my_receive(file_select.currentText(), ntwk_details))
        send_btn.released.connect(lambda: self.c.my_send(send_input.text(), ntwk_details))

        self.setLayout(self.main_layout)

    def connect(self, host, port, conn_details, conn_label):
        if self.c.connected:
            conn_details.setText("Already Connected")
            return

        if self.c.connecting:
            conn_details.setText("Already trying to connect...")
            return

        host_passed = True
        for octet in host.split('.'):
            if not octet.isdigit():
                conn_details.setText("Host is not a ipv4")
                host_passed = False

        if not port.isdigit():
            if not host_passed:
                conn_details.setText(conn_details.text() + "\nPort is not a number")
                return
            conn_details.setText("Port is not a number")
            return

        # Connect on different thread so program doesn't freeze
        thread = threading.Thread(target=self.c.connect, args=[host, int(port), conn_details, conn_label])
        thread.start()

    def browse(self, path_label):
        file_name = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        path_label.setText(file_name[0])


class Client(object):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.connecting = False

    def connect(self, host, port, conn_details, conn_label):
        self.connecting = True
        conn_details.setText("Connecting...")

        try:
            self.sock.connect((host, port))
        except TimeoutError as err:
            conn_details.setText("Host did not respond in time")
            return
        except ConnectionRefusedError as err:
            conn_details.setText("Host refused connection")
            return
        finally:
            conn_label.setStyleSheet('QLabel#conn_label {color: red}')
            conn_label.setText("Disconnected")
            self.connecting = False

        self.connected = True
        conn_label.setText("Connected")
        conn_label.setStyleSheet('QLabel#conn_label {color: green}')
        conn_details.setText("Connected Successfully")

    def disconnect(self, conn_label, conn_details):
        if not self.connected:
            conn_details.setText("Can't disconnect if not connected")
            return

        self.sock.send('q'.encode("utf-8"))
        self.connected = False
        conn_label.setText("Disconnected")
        conn_label.setStyleSheet("QLabel#conn_label {color: red}")
        conn_details.setText("Successfully Disconnected")

    def my_send(self, file_path, netwk_details):
        print("Trying to send")
        if not self.connected:
            netwk_details.setText("Not Connected")
            return

        # Send a send file request
        self.sock.send('s'.encode('utf-8'))

        # get file name from path
        split_path = file_path.split('/')
        filename = split_path[len(split_path)-1]
        print(filename)
        try:
            filename.split('.')[1]
        except IndexError as err:
            netwk_details.setText("No file found in path " + file_path)
            return

        print("Found file")

        # Get total size in bytes of file
        total_bytes = os.stat(file_path).st_size

        print("Total bytes " + str(total_bytes))

        # Send file length
        self.sock.send(str(total_bytes).encode("utf-8"))

        # send filename
        self.sock.send(filename.encode("utf-8"))

        # Open file in binary mode and read into bytes
        f = open(file_path, "r")

        read_size = 8192
        bytes_sent = 0
        # Send all data
        while bytes_sent < total_bytes:
            n_bytes = self.sock.send(f.read(read_size).encode("utf-8"))
            if not n_bytes:
                netwk_details.setText("Couldn't send all data\n Sent " + str(total_bytes) + "/" + str(bytes_sent))
                return
            bytes_sent += n_bytes

        f.close()

        netwk_details.setText("Successfully sent all data")

    def request_file_names(self, dropdown):
        if not self.connected:
            print("Cannot receive file names if not connected")
            return

        # Send File name request
        self.sock.send('f'.encode("utf-8"))

        # Get message length
        total_bytes = self.sock.recv(512)
        total_bytes = int(total_bytes.decode("utf-8"))

        # Loop until all data is received
        total_recv = 0
        chunks = []
        while total_recv < total_bytes:
            chunk = self.sock.recv(8192)
            if not chunk:
                print("Didn't receive all data")
                return
            chunks.append(chunk)
            total_recv += len(chunk)
        print("Successfully received file names")
        str_filenames = b''.join(chunks).decode("utf-8")
        server_files = str_filenames.split(',')

        for files in server_files:
            dropdown.addItem(files)

    def my_receive(self, file_name, ntwk_details):
        if not file_name.split('.')[1]:
            ntwk_details.setText("No file detected")
            return

        # Send a file request to the server
        self.sock.send('r'.encode("utf-8"))

        # Send file name
        self.sock.send(file_name.encode("utf-8"))

        # Get total file length in bytes
        total_bytes = self.sock.recv(512)
        total_bytes = int(total_bytes.decode("utf-8"))
        print(total_bytes)

        # Create loop to collect all data
        total_recv = 0
        chunks = []
        while total_recv < total_bytes:
            data = self.sock.recv(8192)
            if not data:
                ntwk_details.setText("Lost connection and only received " +
                                     str(total_recv) + '/' + str(total_bytes) + " bytes")
                return
            chunks.append(data)
            total_recv += len(data)
        print(chunks)

        # Save chunks to file
        with open(file_name, 'wb') as f:
            f.write(b''.join(chunks))

        ntwk_details.setText("Successfully received all data\nSaved to file named '" + file_name + "'")


class ipLineEdit(QWidget):

    line_edits = []
    spacers = '.'

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        q_reg = QRegExp("\d{3}")
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        for x in range(4):
            line_edit = QLineEdit()
            q_validator = QRegExpValidator(q_reg, line_edit)
            line_edit.setValidator(q_validator)
            line_edit.setFont(QFont(None, 13))
            line_edit.setMaximumWidth(35)
            line_edit.setMinimumWidth(35)

            self.layout.addWidget(line_edit)
            if x < 3:
                self.layout.addWidget(QLabel("."))

            self.line_edits.append(line_edit)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def text(self):
        text = []
        for line_edit in self.line_edits:
            text.append(line_edit.text())
        return '.'.join(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Gui()
    sys.exit(app.exec())
