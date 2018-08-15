#!/usr/bin/python


import socket
import pickle
import sys

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


class Block:
    def __init__(self, transactions, hashPrevBlock):
        self.transactions = transactions
        self.hashPrevBlock = hashPrevBlock
        self.nonce = None

transactionQueue= []

def AddToTransactionQueue(data):
     transactionQueue.append(data)


def RecTransaction():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ""
    port = 11111


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

            while True:
                data = connection.recv(1024)
                data = pickle.loads(data)
                print('received {!r}'.format(data))
                break
            if(data.find("end") == True):
                break                
            else:
                AddToTransactionQueue(data)
                pass          

        finally:
            # Clean up the connection
            connection.close()
        if(data.find("end") == True):
                break

recTransaction()

