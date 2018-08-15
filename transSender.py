import socket
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

def SendDataToOneNodeWithEND(data, ip):
    SendDataToOneNode(data, ip)
    end = transaction("end", "end")
    SendDataToOneNode(end, ip)

def SendDataListToOneNodeWithEND(data, ip):
    SendDataListToOneNode(data, ip)
    end = transaction("end", "end")
    SendDataToOneNode(end, ip)

    
def SendDataToAllNodes(data):
    for ip in bChainServerList:
        SendDataToOneNode(data, ip)


def SendDataToAllNodesWithEND(data):
    SendDataToAllNodes(data)
    end = transaction("end", "end")
    SendSingleTransactionToAllNodes(end)

def SendDataListToAllNodes(data):
    for ip in bChainServerList:
        SendDataToOneNode(data, ip)


def SendDataListToAllNodesWithEND(data):
    SendDataListToAllNodes(data)
    end = transaction("end", "end")
    SendSingleTransactionToAllNodes(end)




SendDataListToOneNode(transactionQueue, "")
SendDataToOneNode(ideja, "")
SendDataToOneNode(blok, "")

