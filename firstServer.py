#!/usr/bin/python
DEBUG = False

from socket import *
import asyncio
import pickle
import time
import os
from BlockChainDataStruct import *
from DataTransferFuns import *


def RefreshTransactionQueue(block):
    for i in block.transactions:
        if(i in transactionQueue):
            index = transactionQueue.index(i)
            del transactionQueue[index]

def StartMining():
    os.system('python3 miner.py &')
    time.sleep(3)
    SendDataListToOneNode(transactionQueue, "", 22222)
    if(DEBUG):
        print(blockChain[-1].hashIt())
    SendDataToOneNode(blockChain[-1].hashIt(), "", 22222)

def StopMining():
    try:
        pid = os.popen("ps aux | grep miner.py | awk '{print $2}'").readlines()[0] #call pid
        os.system('kill '+pid) #kill process
    except:
        print("nije se ni minealo")

def PingServer(state, ip):
    host = ip
    print(host)                       
    port = 9999
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))
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
    if(DEBUG):
        print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)
    
    # Listen for incoming connections
    sock.listen(10)

    while True:
        # Wait for a connection
        if(DEBUG):
            print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            if(DEBUG):
                print('connection from', client_address)

            while True:
                data = connection.recv(1024)
                data = pickle.loads(data)
                if(DEBUG):
                    print('received {!r}'.format(data))
                break
        
            if(data == "endThisSession"):
                pass
            elif(data.dataType() == "transaction"):

                if(client_address[0] == '127.0.0.1'):
                    if(DEBUG):
                        print("transakcija je moja")
                    AddToTransactionQueue(data)
                    for i in bChainServersList:
                        if(i != '127.0.0.1'):
                            time.sleep(1)
                            if(DEBUG):
                                print("------------------pingam")
                            PingServer("TRANS", i)
                            time.sleep(1)
                            if(DEBUG):
                                print("-----------------saljem")
                            SendDataToOneNode(data, i, 9898)
                            time.sleep(1)
                            if(DEBUG):
                                print("---------zavrsavam")
                            SendDataToOneNode("endThisSession", i, 9898)
                else:
                    if(DEBUG):
                        print("transakcija nije moja")
                    AddToTransactionQueue(data)
            elif(data.dataType() == "block"):
                if(client_address[0] == '127.0.0.1'):
                    if(DEBUG):
                        print("block je moj")
                    AddToBlockChain(data)
                    ##posalji svima ostalima
                    for i in bChainServersList:
                        if(i != '127.0.0.1'):
                            PingServer("BLOCK", i)
                            SendDataToOneNode(data, i, 9898)
                            SendDataToOneNode("endThisSession", i, 9898)
                    RefreshTransactionQueue(data)
                    StartMining()
                else:
                    if(DEBUG):
                        print("block nije moj")
                    StopMining()
                    AddToBlockChain(data)
                    RefreshTransactionQueue(data)
                    StartMining()
            else:
                pass          

        finally:
            # Clean up the connection
            connection.close()
            if(data == "endThisSession"):
                break

def InitMe():
    host = str(input("Enter ip addr of one node on the p2p blockchain network"))                     
    port = 9999
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))
    s.sendall("INIT".encode('latin-1').strip())
    s.close()
    RecTransaction(9898)


def AddNewNodeToBChain(addr, loop):##
    if(DEBUG):
        print("AddNewNodeToBChain\n")
    if(addr[0] not in bChainServersList):
        if(addr[0] != '127.0.0.1'):
            SendDataListToOneNode(blockChain, addr[0], 9898)##novom članu šaljemo cijeli blockchain
            SendDataListToOneNode(transactionQueue, addr[0], 9898)
            SendDataListToOneNode(bChainServersList, addr[0], 9898)##saljemo novom nodeu sve ostale
            SendDataToAllNodes("NEW,"+addr[0], 9898) ##saljemo svim starim nodeovima novog
    bChainServersList.append(addr[0])
    SendDataToOneNode("endThisSession",addr[0], 9898)
    if(DEBUG):
        print("KRAJ AddNewNodeToBChain\n")
    return

async def Glavna_funkcija_programa(address, loop):
    if(DEBUG):
        print("Glavna_funkcija_programa")
        print(bChainServersList)
        print(blockChain)
        print(transactionQueue)
    ##
    ##ovdje bi svi osim prvog prvo trebali skupit cijeli ledger
    #InitMe() ##ve req all ip addr and the whole ledgger
    ##
    StartMining()
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(10)
    sock.setblocking(False)

    if(DEBUG):
        print(bChainServersList)
        print(blockChain)
        print(transactionQueue)
    print("ready...")
    while True:
        if(DEBUG):
            print("Ulaz u beskonacnu petlju")
            print("###########        #########sve transakcije")
            print(transactionQueue)
        client, addr = await loop.sock_accept(sock)
        if(DEBUG):
            print('Connection from', addr)
        loop.create_task(request_handler(client, addr, loop))
        if(DEBUG):
            print(transactionQueue)
    sock.close()

async def request_handler(client, addr, loop):
    global data
    if(DEBUG):
        print("request handler")
    data = await loop.sock_recv(client, 1024)
    if(DEBUG):
        print("$$$$$$$data")
        print(data)
    data = data.decode()
    if(DEBUG):
        print("$$$$$$$data")
        print(data)
    (REQ, data) = CheckReq(data)
    if(DEBUG):
        print("######REQ")
        print("#data")
        print("primio sam {}", format(data))

    if REQ == "INIT":
        if(DEBUG):
            print("#########usao sam u INIT")
        time.sleep(2)
        AddNewNodeToBChain(addr, loop)  
    elif REQ == "NEW":
        if(DEBUG):
            print("#########usao sam u NEW")
        time.sleep(2)
        bChainServersList.append(data)
        #dosao je novi član u p2p mrežu, dodamo ga na popis ip addr
        #ovo je scenarij kada drugi node inicijalizira novi node a nas samo obavjesti da je novi nod usao u mrežu
        pass
    elif REQ == "TRANS":
        if(DEBUG):
            print("#########usao sam u TRANS")
        RecTransaction(9898)
        
    elif REQ == "OURTRANS":
        if(DEBUG):
            print("#########usao sam u OURTRANS")
        RecTransaction(11111)
    elif REQ == "BLOCK":
        if(DEBUG):
            print("#########usao sam u BLOCK")
        RecTransaction(9898)
    else:
        pass
    if(DEBUG):
        print('Connection closed')
    print(transactionQueue)
    for block in blockChain:
        block.display()
    
    client.close()
    print("ready...")

def RecsieverMainFunction():
    loop = asyncio.get_event_loop()
    
    server = loop.run_until_complete(Glavna_funkcija_programa(('', 9999), loop))
    
    loop.run_forever()
        
    server.close()

def Main():
    RecsieverMainFunction()

bChainServersList = []
ideja = Transaction("ante", "Zivot je kratak pojedi batak")
ideja2 = Transaction("ivan", "placi, placi.. manje ces pisati")

transactionQueue = [ideja, ideja2]

blok = Block([ideja,ideja2], 33333)

blockChain = [blok]

if __name__ == '__main__':
    Main()
