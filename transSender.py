import socket
import pickle
import time

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
    

ideja = Transaction("ante", "KOD NAS SVI SE ZOVU ANTE")
ideja2 = Transaction("ivan", "placi, placi.. manje ces pisati")

transactionQueue = [ideja, ideja2]
print(transactionQueue)
blok = Block(ideja, 33333)

def SendDataToOneNode(data, ip, port):
# Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (ip, port)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:

        # Send data
        
        message = pickle.dumps(data)#.('utf-8')
        print('sending {!r}'.format(message))
        sock.sendall(message)


    finally:
        print('closing socket')
        sock.close()

def SendDataListToOneNode(data, ip, port):
    for i in data:
        SendDataToOneNode(i, ip, port)


    
def SendDataToAllNodes(data, port):
    for ip in bChainServerList:
        SendDataToOneNode(data, ip, port)


def SendDataListToAllNodes(data, port):
    for ip in bChainServerList:
        SendDataToOneNode(data, ip, port)


def PingServer(state, portNum):
    host = ""
    print(host)                       
    port = portNum
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port)) 
    s.sendall(state.encode('latin-1'))
    s.close()
    time.sleep(5)


#PingServer("TRANS")
PingServer("OURTRANS", 9999)
#autor = input("unesire kreatora: ")
#ideja = input("velika ideja: ")
#transakcija = Transaction(autor, ideja)
transakcija = Transaction("a#####################nte", "lupa kante")
SendDataToOneNode(transakcija, "",11111)

SendDataToOneNode("endThisSession", "", 11111)
    

