from socket import *
import asyncio
import pickle
import time
import os


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
    SendDataListToOneNode(transactionQueue, "", 9899)

def StopMining():
    pid = os.popen("ps aux | grep miner.py | awk '{print $2}'").readlines()[0] #call pid
    os.system('kill '+pid) #kill process

def PingServer(state, ip):
    host = ip
    print(host)                       
    port = 9999
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))
    time.sleep(0.5)
    s.sendall(state.encode('latin-1').strip())
    s.close()
    time.sleep(5)

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
                            time.sleep(1)
                            print("------------------pingam")
                            PingServer("TRANS", i)
                            time.sleep(5)
                            print("-----------------saljem")
                            SendDataToOneNode(data, i, 9898)
                            time.sleep(1)
                            print("---------zavrsavam")
                            SendDataToOneNode("endThisSession", i, 9898)
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
                            SendDataToOneNode(data, i, 9898)
                            SendDataToOneNode("endThisSession", i, 9898)
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

def InitMe():
    host = str(input("Enter ip addr of one node on the p2p blockchain network"))       
    print(host)                       
    port = 9999
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))
    s.sendall("INIT".encode('latin-1').strip())
    s.close()
    RecTransaction(9898)


def SendDataToOneNode(data, ip, port):
    sock = socket(AF_INET, SOCK_STREAM)
    server_address = (ip, port)
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

def SendDataToOneNode(data, ip, port):
    print("#########SendDataToOneNode")
    print("# Create a TCP/IP socket")
    sock = socket(AF_INET, SOCK_STREAM)

    print("# Connect the socket to the port where the server is listening")
    server_address = (ip, port)
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

def SendDataListToOneNode(data, ip, port):
    print("#########SendDataListToOneNode")
    for i in data:
        SendDataToOneNode(i, ip, port)

def SendDataToAllNodes(data, port):
    print("######SendDataToAllNodes")
    for ip in bChainServersList:
        if(ip != '127.0.0.1'):
            SendDataToOneNode(data, port)

def AddNewNodeToBChain(addr, loop):##
    print("AddNewNodeToBChain\n")
    if(addr[0] not in bChainServersList):
        if(addr[0] != '127.0.0.1'):
            SendDataListToOneNode(blockChain, addr[0], 9898)##novom članu šaljemo cijeli blockchain
            SendDataListToOneNode(transactionQueue, addr[0], 9898)
            SendDataListToOneNode(bChainServersList, addr[0], 9898)##saljemo novom nodeu sve ostale
            SendDataToAllNodes("NEW,"+addr[0], 9898) ##saljemo svim starim nodeovima novog
    bChainServersList.append(addr[0])
    SendDataToOneNode("endThisSession",addr[0], 9898)
    print("KRAJ AddNewNodeToBChain\n")
    return

async def Glavna_funkcija_programa(address, loop):
    print("Glavna_funkcija_programa")
    print(bChainServersList)
    print(blockChain)
    print(transactionQueue)
    ##
    ##ovdje bi svi osim prvog prvo trebali skupit cijeli ledger
    #InitMe() ##ve req all ip addr and the whole ledgger
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
    print("$$$$$$$data")
    print(data)
    data = data.decode()
    print("$$$$$$$data")
    print(data)
    (REQ, data) = CheckReq(data)
    print("######REQ")
    print("#data")
    print("primio sam {}", format(data))

    if REQ == "INIT":
        time.sleep(2)
        AddNewNodeToBChain(addr, loop)  
    elif REQ == "NEW":
        time.sleep(2)
        bChainServersList.append(data)
        #dosao je novi član u p2p mrežu, dodamo ga na popis ip addr
        #ovo je scenarij kada drugi node inicijalizira novi node a nas samo obavjesti da je novi nod usao u mrežu
        pass
    elif REQ == "TRANS":
        #time.sleep(2)
        print("#########usao sam u TRANS")
        RecTransaction(9898)
    elif REQ == "OURTRANS":
        RecTransaction(11111)
    elif REQ == "BLOCK":
        #time.sleep(2)
        RecTransaction(9898)
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

bChainServersList = []
ideja = Transaction("ante", "Zivot je kratak pojedi batak")
ideja2 = Transaction("ivan", "placi, placi.. manje ces pisati")

transactionQueue = [ideja, ideja2]
print(transactionQueue)
blok = Block(ideja, 33333)

blockChain = []

if __name__ == '__main__':
    Main()
