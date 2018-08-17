import pickle
import time

from socket import *
from BlockChainDataStruct import *
from DataTransferFuns import *

def PingServer(state, portNum):
    host = ""
    print(host)                       
    port = portNum
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port)) 
    s.sendall(state.encode('latin-1'))
    s.close()
    time.sleep(5)

while True:
    PingServer("OURTRANS", 9999)
    autor = input("unesire kreatora: ")
    ideja = input("velika ideja: ")
    transakcija = Transaction(autor, ideja)
    if(autor != "0"):
        SendDataToOneNode(transakcija, "",11111)
        SendDataToOneNode("endThisSession", "", 11111)
    else:
        SendDataToOneNode("endThisSession", "", 11111)
        break
    print("\n\n")
    time.sleep(10)
    

