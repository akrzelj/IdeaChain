#!/usr/bin/python

import time
import socket
import pickle
import sys
import hashlib

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
        self.transactions = [transactions]
        self.hashPrevBlock = hashPrevBlock
        self.nonce = None
    def dataType(self):
        return "block"
    def findEnd(self):
        if(self.transactions.creator == "end"):
            return True
        else:
            return False
    def hashIt(self):
        m = hashlib.new('sha256')
        m.update(pickle.dumps(self))
        tmp = m.hexdigest()
        del m
        return tmp
        


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
            elif(type(data) == type("string") and data.find("hash") == 0):
                data = data.split(",")
                hashPrevBlock = data[1]
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


    difficultieLevel = 10
    targetString = "0000000000"
    noviBlock = Block(transactions, prevHash)
    noviBlock.nonce = 0
    guessNumber = 0

    flag = 1
    nonce = random.randrange(0, 5000000, 2)
    timeStart = time.time()

    while(flag):
        if(True):            
            var = noviBlock.hashIt()
            
            hashPartForChacking = var[:difficultieLevel]
            
            if(hashPartForChacking == targetString):##hit done
                flag = 0
                print("############################FOUND IT############")
                time.sleep(1)
                PingServer("BLOCK")
                time.sleep(1)
                SendDataToOneNode(noviBlock, "")
                time.sleep(1)
                SendDataToOneNode("endThisSession", "")
                time.sleep(10)
                sys.exit("Block is mined... Program is terminating....") ##ugasimo program kad smo izmajnali
                
            else:                                   ##no hit, continue
                guessNumber = guessNumber + 1
                pass
            
        nonce = nonce + 1
        noviBlock.nonce = nonce

def SendDataToOneNode(data, ip):
# Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (ip, 9898)
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
    noviBlock = Block(transactionQueue, hashPrevBlock)
    mine(transactionQueue, hashPrevBlock)
    
hashPrevBlock = ""
transactionQueue= []




main()
