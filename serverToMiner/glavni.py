#!/usr/bin/python
import json
import socket
import pickle
import subprocess
##subprocess.Popen("script2.py 1", shell=True)

class transaction:
    def __init__(self, creator, idea):
        self.creator = creator
        self.idea = idea

    def __repr__(self):
        return str("Ideja: " + self.idea + ", autor: " + self.creator + ".\n")

    def find(self, someString):
        if(self.creator == "end"):
            return True
        else:
            return False
    

ideja = transaction("ante", "Zivot je kratak pojedi batak")
ideja2 = transaction("ivan", "placi, placi.. manje ces pisati")

transactionQueue = [ideja, ideja2]
print(transactionQueue)

def recBlock():
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
port = 41111


    # Bind the socket to the port
    server_address = (host, port)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(1024)
                data = pickle.loads(data)
                print('received {!r}'.format(data))
                break
            if(data.find("end") == True):
                break
            else:
                #addToBChain(data)
            

        finally:
            # Clean up the connection
            connection.close()
        if(data.find("end") == True):
                break


def SendSingleTransactionsToMiner(data):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ("", 41111)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:

        # Send data
        message = pickle.dumps(data)#.encode('utf-8')
        print('sending {!r}'.format(message))
        sock.sendall(message)


    finally:
        print('closing socket')
        sock.close()


def SendTransactionsToMiner(transactionQueue):
    for i in transactionQueue:
        print(i)
        SendSingleTransactionsToMiner(i)
    end = transaction("end", "end")
    SendSingleTransactionsToMiner(end)

SendTransactionsToMiner(transactionQueue)
RecBlock()

