import socket
from os import getcwd
# import threading
# import logging
from sys import exit, argv
from pathlib import Path
from Parser import exprParse

'''logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


def receive(sock: socket.socket):
    logging.debug("start")
    while True:
        data = sock.recv(1024)
        if not data: exit(0)
        logging.debug("received")
        print('\n' + data.decode("utf-8"))
        print("=>")

'''

"""try:
    print(argv[0], argv[1])
except IndexError:
    print("use: python 'file' IP PORT")
"""

# client.connect(("192.168.183.186", PORT+1))
# recvThread = threading.Thread(target=receive, args=(client,), ).start()line=file.read(1024)
#client.connect(('192.168.1.32', 4445))
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((argv[1], int(argv[2])))
password = input("input password: ")
client.sendall(password.encode('utf-8'))
response = client.recv(2048).decode("utf-8")
if response[0] == "I":
    print(response)
    client.close()
    exit(0)
files = client.recv(1024).decode('utf-8')
print(files)
fileExpr = input("input number of wanted file: ")
queue = exprParse(fileExpr)
while True:
    try:
        client.send(str(queue.popleft()).encode('utf-8'))
        filename = client.recv(1024)
        with open(Path(getcwd() + "/{}".format(filename.decode('utf-8'))), 'wb') as file:
            line = client.recv(1024)
            while line != b'$$$':
                if b'$$$' in line:
                    file.write(line[:-3])
                    break
                else:
                    file.write(line)
                line = client.recv(1024)

    except IndexError:
        client.sendall('0'.encode('utf-8'))
        print("all files received")
        client.shutdown(2)
        client.close()
        break



