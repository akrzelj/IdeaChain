#!/usr/bin/python
DEBUG = False

from socket import *
import pickle


def SendDataToOneNode(data, ip, port):
    sock = socket(AF_INET, SOCK_STREAM)
    server_address = (ip, port)
    if(DEBUG):
        print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    try:
        # Send data
        message = pickle.dumps(data)#.encode('utf-8')
        if(DEBUG):
            print('sending {!r}'.format(message))
        sock.sendall(message)
    finally:
        if(DEBUG):
            print('closing socket')
        sock.close()

def SendDataToOneNode(data, ip, port):
    if(DEBUG):
        print("#########SendDataToOneNode")
        print("# Create a TCP/IP socket")
    sock = socket(AF_INET, SOCK_STREAM)
    if(DEBUG):
        print("# Connect the socket to the port where the server is listening")
    server_address = (ip, port)
    if(DEBUG):
        print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    try:
        # Send data
        message = pickle.dumps(data)#.encode('utf-8')
        if(DEBUG):
            print('sending {!r}'.format(message))
        sock.sendall(message)
    finally:
        if(DEBUG):
            print('closing socket')
        sock.close()

def SendDataListToOneNode(data, ip, port):
    if(DEBUG):
        print("#########SendDataListToOneNode")
    for i in data:
        SendDataToOneNode(i, ip, port)

def SendDataToAllNodes(data, port):
    if(DEBUG):
        print("######SendDataToAllNodes")
    for ip in bChainServersList:
        if(ip != '127.0.0.1'):
            SendDataToOneNode(data, port)
