from threading import Thread
from socket import *
import asyncio
import json
import pickle

class Block:
    def __init__(self, number):
        self.number = number #placeholder for the real imp


class Transaction:
    def __init__(self, data):
        self.sender = data[0]
        self.recsiever = data[1]
        self.amount = int(data[2])

ip = '127.0.0.1'

bChainServersList = []
##fillers for testing
bChainServersList.append("127.0.0.5")
bChainServersList.append("127.0.0.5")
bChainServersList.append("127.0.0.4")
bChainServersList.append("127.0.0.2")
bChainServersList.append("127.0.0.3")

##test helper
controlList = ["0.0.0.0"]

blockChain = [] #list for storing blocks

transactionQueue = [] #transactions which are not in mining proces

def AddBlockToBlockChain(data):#placeholder
    tmpBlock = Block(data)
    blockChain.append(tmpBlock)

def CheckReq(data): #helper for handling incomming REQs
    tmp = list(data.split(","))
    if(tmp[0].find("INIT") == 0):
        return (tmp[0], tmp[1:])
    elif(tmp[0].find("TRANS") == 0):
        return (tmp[0], tmp[1:])
    elif(tmp[0].find("BLOCK") == 0):
        return (tmp[0], tmp[1:])
    else:
        return "WRONG REQ"

def AddTransactionToQueue(data):
    tmpTrans = Transaction(data) #raw data to Transaction obj
    ##checkTrans(tmpTrans) chck if there are enough coins
    transactionQueue.append(tmpTrans)

async def SendAllIpAddrToNewNode(addr, loop):
    print("Entering SendAllIpAddrToNewNode\n") ##prints like this are for debuggins purposes
    noviSocket = socket(AF_INET, SOCK_STREAM)
    noviSocket.connect((addr[0], 30000))

    b = json.dumps(bChainServersList).encode('utf-8')
    await loop.sock_sendall(noviSocket, b)

    noviSocket.close()
    print("zavrsio SendAllIpAddrToNewNode\n")

async def SendControlList(addr, loop):#saljemo kada je novi server
    print("Send Control List\n")   #vec inicijaliziran
    noviSocket = socket(AF_INET, SOCK_STREAM)
    noviSocket.connect((addr[0], 30000))

    b = json.dumps(controlList).encode('utf-8')##formatiramo podatke koje saljemo
    await loop.sock_sendall(noviSocket, b)##posaljemo mu sve podatke

    noviSocket.close()
    print("zavrsio send control list\n")
    return

async def AddToBChain(addr, loop):
    print("Add To BChain\n")
    for i in bChainServersList:
        if i == addr[0]: ##ovdje valjda treba biti !=
            loop.create_task(SendControlList(addr, loop))
            return
        
    bChainServersList.append(addr[0])
    loop.create_task(SendAllIpAddrToNewNode(addr, loop))##saljemo novom sve ostale
    ##posalji novoga svim ostalima#############################
    print("KRAJ Add to BChain")
    return

async def Glavna_funkcija_programa(address, loop):
    print("Glavna_funkcija_programa")
    ##
    ##ovdje bi svi osim prvog prvo trebali skupit cijeli ledger
    ##
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    sock.setblocking(False)
    while True:
        print("Ulaz u beskonacnu petlju")
        client, addr = await loop.sock_accept(sock)
        print('Connection from', addr)
        loop.create_task(request_handler(client, addr, loop))
    sock.close()

async def request_handler(client, addr, loop):
    global data
    print("request handler")
    data = await loop.sock_recv(client, 1024)

    data = data.decode()
    (REQ, data) = CheckReq(data)
    print("primio sam {}", format(data))

    if REQ == "INIT":
        loop.create_task(AddToBChain(addr, loop))

    elif REQ == "TRANS":
        ##ako je nasa transakcija sljemo je svima ostalima
        ##posaljiTransakcijuSvimaOstalima()
        ##ako je tudja
        ##AddTransactionToQueue(data)
        pass

    elif REQ == "BLOCK":
        ##primamo block
        ##ako je nas blok onda ga prosljedjujemo svima ostalima
        ##ako je tudji dodajemo ga u blockChain
        AddBlockToBlockChain(data)
        print("Jedi govna bloče")
        pass
    else:
        pass
    print('Connection closed')
    client.close()

def RecsieverMainFunction():
    loop = asyncio.get_event_loop()
    loop2 = asyncio.get_event_loop()
    
    server = loop.run_until_complete(Glavna_funkcija_programa(('', 9999), loop))
    
    loop.run_forever()
        
    server.close()

def Main():
    RecsieverMainFunction()

if __name__ == '__main__':
    Main()