#!/usr/bin/python


import socket
import pickle
import sys

class Transaction:
    def __init__(self, creator, idea):
        self.creator = creator
        self.idea = idea

    def __repr__(self):
        return str("Ideja: " + self.idea + ", autor: " + self.creator + ".\n")

    def findEnd(self):
        if(self.creator == "end"):
            return True
        else:
            return False
    def dataType(self):
        return "transaction"


class Block:
    def __init__(self, transactions, hashPrevBlock):
        self.transactions = transactions
        self.hashPrevBlock = hashPrevBlock
        self.nonce = None
    def dataType(self):
        return "block"
    def findEnd(self):
        if(self.transactions.creator == "end"):
            return True
        else:
            return False



transactionQueue= []
blockChain = []
bChainServersList = ["127.0.0.5", "ydsds"]



def AddToBlockChain(data):
    blockChain.append(data)
    


def AddToTransactionQueue(data):
    transactionQueue.append(data)


def RecTransaction():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ""
    port = 9990

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
                print("prvo")
                print(type(data))
                data = pickle.loads(data)
                print("drugo")
                print(type(data))
                print('received {!r}'.format(data))
                print(type(data) == type("string"))
                break
            if(data == "endThisSession"):
                pass
            elif(type(data) == type("string")):
                print(data)
                bChainServersList.append(data)
            else:
                if(data.dataType() == "transaction"):
                    AddToTransactionQueue(data)
                elif(data.dataType() == "block"):
                    AddToBlockChain(data)
                else:
                    pass          

        finally:
            # Clean up the connection
            connection.close()
            if(data == "endThisSession"):
                break





def InitMe():
    host = ""       
    print(host)                       
    port = 9999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port)) 
    s.sendall("INIT".encode('ascii'))
    s.close()
    RecTransaction()
print(bChainServersList)
print(blockChain)
print(transactionQueue)

InitMe()

print(bChainServersList)
print(blockChain)
print(transactionQueue)

