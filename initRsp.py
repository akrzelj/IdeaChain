from socket import *
import pickle

bChainServersList = []
##fillers for testing
##izmjena blockova i transakcija ide na portu 11111
bChainServersList.append("127.0.0.5")
bChainServersList.append("127.0.0.5")
bChainServersList.append("127.0.0.4")
bChainServersList.append("127.0.0.2")
bChainServersList.append("127.0.0.3")



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
    

ideja = Transaction("ante", "Zivot je kratak pojedi batak")
ideja2 = Transaction("ivan", "placi, placi.. manje ces pisati")

transactionQueue = [ideja, ideja2]
print(transactionQueue)
blok = Block(ideja, 33333)

def SendDataToOneNode(data, ip):
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
        sock.sendall(message)


    finally:
        print('closing socket')
        sock.close()

def SendDataListToOneNode(data, ip):
    print("#########SendDataListToOneNode")
    for i in data:
        SendDataToOneNode(i, ip)

    
def SendDataToAllNodes(data):
    for ip in bChainServerList:
        SendDataToOneNode(data, ip)



def SendDataListToAllNodes(data):
    for ip in bChainServerList:
        SendDataToOneNode(data, ip)


def initNode():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('',9999))
    sock.listen(1)

    client, address = sock.accept()
    print(client)
    print(address)

    SendDataListToOneNode(bChainServersList, address[0])
    SendDataListToOneNode(transactionQueue, address[0])
    SendDataToOneNode(blok, address[0])
    SendDataToOneNode("endThisSession", address[0])

initNode()
