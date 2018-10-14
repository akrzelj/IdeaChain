#!/usr/bin/python
FIRST_SERVER = True #only the first server on the blockchain has FIRST_SERVER == True
INIT_ONGOING = True

import asyncio
import pickle
import time
import os
from BlockChainDataStruct import *
from DataTransferFuns import *
from socket import *
import pickle
import datetime

def timestamp():
    now = datetime.datetime.now()
    print ("Current date and time : ")
    print (now.strftime("%Y-%m-%d %H:%M:%S"))

difficultieLevel = 6
targetString = "0" * difficultieLevel

def ValidateBlock(block):
    if(INIT_ONGOING):
        return True
    if(block.hashPrevBlock == blockChain[-1].hashIt()):
        tmp = block.hashIt()
        tmp = tmp[:difficultieLevel]
        if(tmp == targetString):
            return True
        else:
            return False
    else:
        return False

def RefreshTransactionQueue(block):
    global transactionQueue
    for i in block.transactions:
        for j in transactionQueue:
            if (i.creator == j.creator and i.idea == j.idea):
                index = transactionQueue.index(j)
                del transactionQueue[index]

def StartMining():
    os.system('python3 miner.py &')
    time.sleep(3)
    SendDataListToOneNode(transactionQueue, "", 22222)
    SendDataToOneNode(blockChain[-1].hashIt(), "", 22222)
    SendDataToOneNode("endThisSession", "", 22222)

def StopMining():
    try:
        pid = os.popen("ps aux | grep miner.py | awk '{print $2}'").readlines()[0] #call pid
        os.system('kill '+pid) #kill process
    except:
        print("miner was not active")

def PingServer(state, ip):
    port = 9999
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((ip, port))
    time.sleep(0.5)
    s.sendall(state.encode('latin-1').strip())
    s.close()
    time.sleep(3)

def CheckReq(data): #helper for handling incomming REQs
    tmp = list(data.split(","))
    if(tmp[0].find("INIT") == 0):
        return (tmp[0], tmp[1:])
    if(tmp[0].find("NEW") == 0):
        return (tmp[0], tmp[1:])
    elif(tmp[0].find("TRANS") == 0):
        return (tmp[0], tmp[1:])
    elif(tmp[0].find("OURTRANS") == 0):
        return (tmp[0], tmp[1:])
    elif(tmp[0].find("BLOCK") == 0):
        return (tmp[0], tmp[1:])
    else:
        return "WRONG REQ"

def AddToBlockChain(data):
    blockChain.append(data) 

def AddToTransactionQueue(data):
     transactionQueue.append(data)


def RecTransaction(portNum):
    sock = socket(AF_INET, SOCK_STREAM)
    host = ""
    port = portNum

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
            if(type(data) == type([])):
                print("primam listu servera")
                for i in data:
                    bChainServersList.append(i)
            if(data == "endThisSession"):
                pass
            elif(data.dataType() == "transaction"):

                if(client_address[0] == '127.0.0.1'):
                    print("my transaction")
                    timestamp()
                    print(data)
                    AddToTransactionQueue(data)
                    if(bChainServersList):
                        print("Sending to all other nodes")
                        print("svi drugi:")
                        print(bChainServersList)
                        for i in bChainServersList:
                            if(i != '127.0.0.1'):
                                time.sleep(1)
                                PingServer("TRANS", i)
                                time.sleep(1)
                                SendDataToOneNode(data, i, 9898)
                                time.sleep(1)
                                SendDataToOneNode("endThisSession", i, 9898)
                else:
                    print("not my transaction")
                    timestamp()
                    print(data)
                    AddToTransactionQueue(data)
            elif(data.dataType() == "block"):
                if(ValidateBlock(data) == True):
                    if(client_address[0] == '127.0.0.1'):
                        print("my block")
                        AddToBlockChain(data)
                        if(bChainServersList):
                            print("sending to all other nodes this block:")
                            timestamp()
                            data.display()
                            for i in bChainServersList:
                                if(i != '127.0.0.1'):
                                    PingServer("BLOCK", i)
                                    SendDataToOneNode(data, i, 9898)
                                    SendDataToOneNode("endThisSession", i, 9898)
                    else:
                        print("not my block")
                        timestamp()
                        data.display()
                        StopMining()
                        AddToBlockChain(data)
                    RefreshTransactionQueue(data)
                    StartMining()
                else:
                    print("Block is not valid")
            else:
                pass          

        finally:
            # Clean up the connection
            connection.close()
            if(data == "endThisSession"):
                break
    sock.close()

def InitMe():
    ip = str(input("Enter ip addr of one node on the p2p blockchain network: "))
    bChainServersList.append(ip)
    PingServer("INIT", ip)
    RecTransaction(9898)


def AddNewNodeToBChain(addr, loop):##
    print("AddNewNodeToBChain\n")
    
    if(addr[0] != '127.0.0.1'):
        SendDataListToOneNode(blockChain, addr[0], 9898)##send whole ledger to new node
        SendDataListToOneNode(transactionQueue, addr[0], 9898)
        if addr[0] in bChainServersList:
            bChainServersList.remove(addr[0])
        SendDataListToOneNode(bChainServersList, addr[0], 9898)##send all bchain members to new node
        SendDataToAllNodes("NEW,"+addr[0], 9898, bChainServersList) ##send new memeber to all nodes on network
    if(addr[0] not in bChainServersList):
        bChainServersList.append(addr[0])
    SendDataToOneNode("endThisSession",addr[0], 9898)
    return

async def Glavna_funkcija_programa(address, loop):
    ##
    ##only the first server does not require initilization
    if(not FIRST_SERVER):
        InitMe() ##receive req all ip addr and the whole ledgger
        print("Init done...")
        print("transaction queue: ")
        print(transactionQueue)
        print("ledger: ")
        for i in blockChain:
            i.display()
    INIT_ONGOING = False
    if(FIRST_SERVER):
        StartMining()
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(10)
    sock.setblocking(False)

    print("ready...")
    while True:
        client, addr = await loop.sock_accept(sock)
        print('Connection from', addr)
        loop.create_task(request_handler(client, addr, loop))
    sock.close()

async def request_handler(client, addr, loop):
    global data
    data = await loop.sock_recv(client, 1024)
    data = data.decode()
    (REQ, data) = CheckReq(data)

    if REQ == "INIT":
        #print("#########usao sam u INIT")
        time.sleep(2)
        AddNewNodeToBChain(addr, loop)  
    elif REQ == "NEW":
        #print("#########usao sam u NEW")
        time.sleep(2)
        bChainServersList.append(data)
        pass
    elif REQ == "TRANS":
        #print("#########usao sam u TRANS")
        RecTransaction(9898)
        
    elif REQ == "OURTRANS":
        #print("#########usao sam u OURTRANS")
        RecTransaction(11111)
    elif REQ == "BLOCK":
       # print("#########usao sam u BLOCK")
        RecTransaction(9898)
    else:
        pass

    
    client.close()
    #print("ready...")

def RecsieverMainFunction():
    loop = asyncio.get_event_loop()
    
    server = loop.run_until_complete(Glavna_funkcija_programa(('', 9999), loop))
    
    loop.run_forever()
        
    server.close()

def Main():
    for i in blockChain:
        i.display()
    RecsieverMainFunction()

if(FIRST_SERVER):
    bChainServersList = []
    ideja = Transaction("Mudar covjek", "Gread idea")
    ideja2 = Transaction("Wise man", "big great idea")
    transactionQueue = [ideja, ideja2]
    blok1 = Block([ideja,ideja2], 33333)
    blok1.nonce = 5
    blok2 = Block([ideja,ideja2], blok1.hashIt())
    blok2.nonce = 30
    blockChain = [blok1, blok2]
    RefreshTransactionQueue(blok2)
else:
    bChainServersList = []
    transactionQueue = []
    blockChain = []

if __name__ == '__main__':
    Main()
