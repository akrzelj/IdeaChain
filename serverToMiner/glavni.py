#!/usr/bin/python
import json
import socket
import pickle
import subprocess
import sys
import os
import time


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
    

ideja = Transaction("ante", "KOD NAS SVI SE ZOVU ANTE")
ideja2 = Transaction("ivan", "placi, placi.. manje ces pisati")

transactionQueue = [ideja, ideja2]
print(transactionQueue)
blok = Block(ideja, 33333)

def SendDataToOneNode(data, ip):
# Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (ip, 22222)
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

    



def StartMining():
    os.system('python3 miner.py &')
    time.sleep(2)
    SendDataListToOneNode(transactionQueue, "")

def StopMining():
    pid = os.popen("ps aux | grep miner.py | awk '{print $2}'").readlines()[0] #call pid
    os.system('kill '+pid) #kill process


StopMining()

