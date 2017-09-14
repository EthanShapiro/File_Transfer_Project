import os
import sys

s = []
for x in range(3):
    s.append("asdfa".encode("utf-8"))
print(s)
s = b','.join(s)
print(s)

def foo(n):
    for x in range(10):
        yield n + x

path = os.getcwd()
print(path)
path = path + "\\test_file.txt"
print(path.split("\\"))
