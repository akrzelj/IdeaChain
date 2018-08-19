#!/usr/bin/python

import time
import socket
import pickle
import sys
import hashlib
from socket import *
from BlockChainDataStruct import *
from DataTransferFuns import *

def AddToBlockChain(data):
    blockChain.append(data) 

def AddToTransactionQueue(data):
     transactionQueue.append(data)

def RecTransaction():
    sock = socket(AF_INET, SOCK_STREAM)
    host = ""
    port = 22222

    # Bind the socket to the port
    server_address = (host, port)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(10)

    while True:
        # Wait for a connection

        connection, client_address = sock.accept()
        try:
            while True:
                data = connection.recv(1024)
                data = pickle.loads(data)
                break

            if(data == "endThisSession"):
                pass
            elif(type(data) == type("string")):
                global hashPrevBlock
                hashPrevBlock = data
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


    difficultieLevel = 7
    targetString = "0000000"
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
                time.sleep(1)
                PingServer("BLOCK")
                time.sleep(1)
                SendDataToOneNode(noviBlock, "", 9898)
                time.sleep(1)
                SendDataToOneNode("endThisSession", "", 9898)
                time.sleep(10)
                sys.exit("Block is mined... Program is terminating....")
                
            else:                                   ##no hit, continue
                guessNumber = guessNumber + 1
                pass
            
        nonce = nonce + 1
        noviBlock.nonce = nonce

def PingServer(state):
    host = ""
    print(host)                       
    port = 9999
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port)) 
    s.sendall(state.encode('ascii'))
    s.close()
    time.sleep(5)

def main():
    RecTransaction()
    mine(transactionQueue, hashPrevBlock)
    
hashPrevBlock = ""
transactionQueue= []

main()
