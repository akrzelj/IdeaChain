from threading import Thread
from socket import *
import asyncio
import json
import pickle
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



def RefreshTransactionQueue(block):
    for i in block.transactions:
        if(i in transactionQueue):
            index = transactionQueue.index(i)
            del transactionQueue[index]


def StartMining():
    os.system('python3 miner.py &')
    time.sleep(2)
    SendDataListToOneNode(transactionQueue, "")

def StopMining():
    pid = os.popen("ps aux | grep miner.py | awk '{print $2}'").readlines()[0] #call pid
    os.system('kill '+pid) #kill process

def PingServer(state, ip):
    host = ip
    print(host)                       
    port = 9999
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port)) 
    s.sendall(state.encode('ascii'))
    s.close()
    time.sleep(5)

bChainServersList = []
##fillers for testing
#bChainServersList.append("127.0.0.5")##server će funkcijonirati na portu 9999


##test helper
controlList = ["0.0.0.0"]

blockChain = [] #list for storing blocks

transactionQueue = [] #transactions which are not in mining proces

# def AddBlockToBlockChain(data):#placeholder
#     tmpBlock = Block(data)
#     blockChain.append(tmpBlock)

def CheckReq(data): #helper for handling incomming REQs
    tmp = list(data.split(","))
    if(tmp[0].find("INIT") == 0):
        return (tmp[0], tmp[1:])
    if(tmp[0].find("NEW") == 0):
        return (tmp[0], tmp[1:])
    elif(tmp[0].find("TRANS") == 0):
        return (tmp[0], tmp[1:])
    elif(tmp[0].find("BLOCK") == 0):
        return (tmp[0], tmp[1:])
    else:
        return "WRONG REQ"

# def AddTransactionToQueue(data):
#     tmpTrans = Transaction(data) #raw data to Transaction obj
#     ##checkTrans(tmpTrans) chck if there are enough coins
#     transactionQueue.append(tmpTrans)
#######################################################################################
##trans rec
def AddToBlockChain(data):
    blockChain.append(data)
    
    

def AddToTransactionQueue(data):
     transactionQueue.append(data)

def SendDataToOneNode(data, ip):
# Create a TCP/IP socket
    sock = socket(AF_INET, SOCK_STREAM)

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


def RecTransaction():
    sock = socket(AF_INET, SOCK_STREAM)
    host = ""
    port = 11111


    # Bind the socket to the port
    server_address = (host, port)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)
    
    # Listen for incoming connections
    sock.listen(10)

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

                if(client_address[0] == '127.0.0.1'):
                    print("transakcija je moja")
                    AddToTransactionQueue(data)
                    for i in bChainServersList:
                        if(i != '127.0.0.1'):
                            PingServer("TRANS", i)
                            SendDataToOneNode(data, i)
                            SendDataToOneNode("endThisSession", i)
                else:
                    print("transakcija nije moja")
                    AddToTransactionQueue(data)
            elif(data.dataType() == "block"):
                if(client_address[0] == '127.0.0.1'):
                    print("block je moj")
                    AddToBlockChain(data)
                    ##posalji svima ostalima
                    for i in bChainServersList:
                        if(i != '127.0.0.1'):
                            PingServer("BLOCK", i)
                            SendDataToOneNode(data, i)
                            SendDataToOneNode("endThisSession", i)
                    RefreshTransactionQueue(data)
                    StartMine()
                else:
                    print("block nije moj")
                    StopMining()
                    AddToBlockChain(data)
                    RefreshTransactionQueue(data)
                    
                    
            else:
                pass          

        finally:
            # Clean up the connection
            connection.close()
            if(data == "endThisSession"):
                break


########################################################################################

def InitRecTransaction():
    sock = socket(AF_INET, SOCK_STREAM)
    host = ""
    port = 9990

    # Bind the socket to the port
    server_address = (host, port)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(10)

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
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port)) 
    s.sendall("INIT".encode('ascii'))
    s.close()
    InitRecTransaction()


#################################################################################################

async def ASendDataToOneNode(data, ip, loop):
    print("#########SendDataToOneNode")
    print("# Create a TCP/IP socket")
    sock = socket(AF_INET, SOCK_STREAM)

    print("# Connect the socket to the port where the server is listening")
    server_address = (ip, 9990)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:

        # Send data
        message = pickle.dumps(data)#.encode('utf-8')
        print('sending {!r}'.format(message))
        await loop.sock_sendall(sock, message)


    finally:
        print('closing socket')
        sock.close()

async def ASendDataListToOneNode(data, ip, loop):
    print("#########SendDataListToOneNode")
    for i in data:
        await ASendDataToOneNode(i, ip, loop)

async def ASendDataToAllNodes(data, loop):
    print("######SendDataToAllNodes")
    for ip in bChainServersList:
        if(ip != '127.0.0.1'):
            await ASendDataToOneNode(data, ip, loop)

async def AAddNewNodeToBChain(addr, loop):##
    print("AddNewNodeToBChain\n")
    if(addr[0] not in bChainServersList):
        if(addr[0] != '127.0.0.1'):
            await ASendDataListToOneNode(blockChain, addr[0], loop)##novom članu šaljemo cijeli blockchain
            await ASendDataListToOneNode(transactionQueue, addr[0], loop)
            await ASendDataListToOneNode(bChainServersList, addr[0], loop)##saljemo novom nodeu sve ostale
            await ASendDataToAllNodes("NEW,"+addr[0], loop) ##saljemo svim starim nodeovima novog
    bChainServersList.append(addr[0])
    await ASendDataToOneNode("endThisSession",addr[0], loop)
    print("KRAJ AddNewNodeToBChain\n")
    return

async def Glavna_funkcija_programa(address, loop):
    print("Glavna_funkcija_programa")
    print(bChainServersList)
    print(blockChain)
    print(transactionQueue)
    ##
    ##ovdje bi svi osim prvog prvo trebali skupit cijeli ledger
    InitMe() ##ve req all ip addr and the whole ledgger
    ##
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(10)
    sock.setblocking(False)
    
    print(bChainServersList)
    print(blockChain)
    print(transactionQueue)
    while True:
        print("Ulaz u beskonacnu petlju")
        print("###########        #########sve transakcije")
        print(transactionQueue)
        client, addr = await loop.sock_accept(sock)
        print('Connection from', addr)
        loop.create_task(request_handler(client, addr, loop))
        print(transactionQueue)
    sock.close()

async def request_handler(client, addr, loop):
    global data
    print("request handler")
    data = await loop.sock_recv(client, 1024)

    data = data.decode()
    (REQ, data) = CheckReq(data)
    print("primio sam {}", format(data))

    if REQ == "INIT":
        loop.create_task(AAddNewNodeToBChain(addr, loop))
    
    elif REQ == "NEW":
        bChainServersList.append(data)
        #dosao je novi član u p2p mrežu, dodamo ga na popis ip addr
        #ovo je scenarij kada drugi node inicijalizira novi node a nas samo obavjesti da je novi nod usao u mrežu
        pass

    elif REQ == "TRANS":
        print("#########usao sam u TRANS")
        RecTransaction()


    elif REQ == "BLOCK":
        RecTransaction()

        
        pass
    else:
        pass
    print('Connection closed')
    client.close()

def RecsieverMainFunction():
    loop = asyncio.get_event_loop()
    
    server = loop.run_until_complete(Glavna_funkcija_programa(('', 9999), loop))
    
    loop.run_forever()
        
    server.close()

def Main():
    RecsieverMainFunction()

if __name__ == '__main__':
    Main()
