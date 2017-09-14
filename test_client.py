import socket
import select

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 5002))
sock.setblocking(0)
print("Waiting to send")
rdy = select.select([], [sock], [], 10)
if rdy[1]:
    print("Sent!")
print("done")