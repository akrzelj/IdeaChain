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
    tmp = input("Press any key")
    PingServer("OURTRANS", 9999)
    autor = input("Creator: ")
    ideja = input("Your idea: ")
    transakcija = Transaction(autor, ideja)
    if(autor != "0"):
        SendDataToOneNode(transakcija, "",11111)
        SendDataToOneNode("endThisSession", "", 11111)
    else:
        SendDataToOneNode("endThisSession", "", 11111)
        break
    print("\n\n\n")
    time.sleep(10)
    

