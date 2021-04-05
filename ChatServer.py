import socket
import threading
from os import listdir
from sys import exit

'''
TODO:
1. password auth DONE
2. regex for files DONE 
3. multiple file upload DONE
4. Hash password
5.
n. Encryption
'''

def receive(sock: socket.socket):
    while True:
        data = sock.recv(1024)
        if not data: exit(0)
        print('\n' + data.decode("utf-8"))



def userAuth(password: str) -> bool:
    # handles simple password authentication
    if password == serverPassword:
        return True
    else:
        return False


def handle_client(connection: socket.socket):
    with connection:
        password = connection.recv(2048).decode('utf-8')
        if not userAuth(password):
            connection.sendall("Incorrect Password! \n".encode('utf-8'))
            connection.shutdown(2)
            connection.close()
            return
        connection.sendall("Welcome To The Filestore!".encode('utf-8'))
        filelist = listdir("./filestore")
        print('Connected to', address)
        strlist = "files available:\n "
        for index, name in enumerate(filelist, 1):
            strlist += ("{0}.- {1}\n".format(index, name))
        try:
            connection.sendall(strlist.encode('utf-8'))
            filenum = connection.recv(1024)
            while filenum != b'0':
                # read filenum from socket, if zero, stop transferring
                filename = filelist[int(filenum.decode('utf-8')) - 1]  # get file from list
                connection.sendall(filename.encode('utf-8'))  # send filename over socket
                with open("filestore/{}".format(filename), 'rb') as file:
                    line = file.read(1024)
                    print(
                        "sending {0} to {1}".format(filename, connection.getpeername()))  # log file transfer to client
                    while line != b'':  # read until EOF
                        connection.sendall(line)
                        line = file.read(1024)
                connection.sendall("$$$".encode('utf-8'))  # EOF identifer
                filenum = connection.recv(1024)  # get new file number



        except KeyboardInterrupt:
            print("\nKilled")
            connection.close()
            server.shutdown(socket.SHUT_RDWR)
            exit(0)

if __name__ == '__main__':
    serverPassword = input("Enter server password:")
    HOST = '127.0.0.1'
    PORT = 4445  # Arbitrary non-privileged port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    print(f'server running on {HOST}:{str(PORT)}')
    server.listen(4)

    while True:
        connection, address = server.accept()
        threading.Thread(target=handle_client, args=(connection,)).start()
