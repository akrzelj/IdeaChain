#!/usr/bin/python

from socket import *
import pickle


def SendDataToOneNode(data, ip, port):
    sock = socket(AF_INET, SOCK_STREAM)
    server_address = (ip, port)
    sock.connect(server_address)
    try:
        # Send data
        message = pickle.dumps(data)#.encode('utf-8')
        sock.sendall(message)
    finally:
        sock.close()

def SendDataListToOneNode(data, ip, port):
    for i in data:
        SendDataToOneNode(i, ip, port)

def SendDataToAllNodes(data, port, bChainServersList):
    for ip in bChainServersList:
        if(ip != '127.0.0.1'):
            SendDataToOneNode(data, ip, port)
