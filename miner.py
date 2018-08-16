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



def AddToBlockChain(data):
    blockChain.append(data)
    
    

def AddToTransactionQueue(data):
     transactionQueue.append(data)


def RecTransaction():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ""
    port = 22222


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
                break
           
        
            if(data == "endThisSession"):
                pass
            elif(data.dataType() == "transaction"):
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



def addToMiningCandidates(data):
    miningCandidates.append(data)
    

def mine(transactions, prevHash):
    import hashlib
    import time
    import random


    difficultieLevel = 6
    targetString = "000000"


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
                
                sendDataToOneNode(noviBlock, "")
                sys.exit("Block is mined... Program is terminating....") ##ugasimo program kad smo izmajnali
                
            else:                                   ##no hit, continue
                guessNumber = guessNumber + 1
                pass
            
            del m
        nonce = nonce + 1

def SendDataToOneNode(data, ip):
# Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (ip, 11111)
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

def SendDataListToOneNode(data, ip):
    for i in data:
        SendDataToOneNode(i, ip)


    
def SendDataToAllNodes(data):
    for ip in bChainServerList:
        SendDataToOneNode(data, ip)


def SendDataListToAllNodes(data):
    for ip in bChainServerList:
        SendDataToOneNode(data, ip)


def PingServer(state):
    host = ""
    print(host)                       
    port = 9999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port)) 
    s.sendall(state.encode('ascii'))
    s.close()
    time.sleep(5)

def main():
    RecTransaction()
    mine()

main()
