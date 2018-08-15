import socket
import pickle

bChainServersList = []
##fillers for testing
bChainServersList.append("127.0.0.5")##server će funkcijonirati na portu 9999
bChainServersList.append("127.0.0.5")
bChainServersList.append("127.0.0.4")
bChainServersList.append("127.0.0.2")
bChainServersList.append("127.0.0.3")



class transaction:
    def __init__(self, creator, idea):
        self.creator = creator
        self.idea = idea

    def __repr__(self):
        return str("Ideja: " + self.idea + ", autor: " + self.creator + ".\n")

    def find(self, someString):
        if(self.creator == "end"):
            return True
        else:
            return False

class BlockBody:
    def __init__(self, transactions, hashPrevBlock):
        self.transactions = transactions
        self.hashPrev = hashPrev

class BlockHeader:
    def __init__(self):
        self.nonce = None

class Block(BlockBody,BlockHeader):
    def __init__(self, transactions, hashPrevBlock):
        BlockBody.__init__(self, transactions, hashPrevBlock)
        BlockHeader.__init__()
    

ideja = transaction("ante", "Zivot je kratak pojedi batak")
ideja2 = transaction("ivan", "placi, placi.. manje ces pisati")

transactionQueue = [ideja, ideja2]
print(transactionQueue)



def SendSingleTransactionToAllNodes(data):
    for i in bChainServerList:
    # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = (i, 11111)
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


def SendSingleTransactionToAllNodesWithEND(data):
    SendSingleTransactionToAllNodes(data)
    end = transaction("end", "end")
    SendSingleTransactionToAllNodes(end)

def SendAllTransactionsToAllNodesWithEND(transactionQueue):
    SendSingleTransactionToAllNodes(transactionQueue)
    end = transaction("end", "end")
    SendSingleTransactionToAllNodes(end)

