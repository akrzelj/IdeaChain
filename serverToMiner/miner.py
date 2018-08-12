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
miningCandidates = []
hashPrevBlock = None



def addToMiningCandidates(data):
    miningCandidates.append(data)
    

def mine(transactions, prevHash):
    import hashlib
    import time
    import random


    difficultieLevel = 5
    targetString = "00000"


    flag = 1
    nonce = random.randrange(0, 500000, 2)
    timeStart = time.time()

    while(flag):
        if(True):
            m = hashlib.new('sha256')
            m.update((noviBlock).encode("utf-8"))##prvo bi trebali updateat sa tijelom blocka
            m.update((hashPrevBlock).encode("utf-8"))
            m.update((str(nonce)).encode("utf-8"))##update sa nonceom
            print("di pusas")
            
            var = m.hexdigest()
            
            hashPartForChacking = var[:difficultieLevel]
            print(hashPartForChacking)
            
            if(hashPartForChacking == targetString):##hit done
                flag = 0
                #zapakiraj nonce u header blocka
                noviBlock.nonce = nonce
                
                sendBlockToServer(noviBlock)
                sys.exit("Block is mined... Program is terminating....") ##ugasimo program kad smo izmajnali
                
            else:                                   ##no hit, continue
                guessNumber = guessNumber + 1
                pass
            
            del m
        nonce = nonce + 1


def sendBlockToServer(data):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ("", 41111)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:

        # Send data
        message = pickle.dumps(data)
        print('sending {!r}'.format(message))
        sock.sendall(message)


    finally:
        print('closing socket')
        sock.close()


def recTransaction():
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

            while True:
                data = connection.recv(1024)
                data = pickle.loads(data)
                print('received {!r}'.format(data))
                break
            if(data.find("end") == True):
                break
            elif(data.find("hash") == True):
                data = data.split(",")
                data = data[1]
                hashPrevBlock = data
                break
                
            else:
                addToMiningCandidates(data)
                pass
            

        finally:
            # Clean up the connection
            connection.close()
        if(data.find("end") == True):
                break

#recTransactions()


noviBlock = Block(miningCandidates, hashPrevBlock)
print(noviBlock.hashPrevBlock)

#mine()
