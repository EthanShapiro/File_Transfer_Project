import socket
import select

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 5002))
sock.listen(1)
sock.setblocking(0)
print("Server on...")

print("Waiting for timeout or connection")
ready = select.select([sock], [], [], 10)
print("blah")
if ready[0]:
    print("Ready to recieve!")
print("Timed out")
