#!/usr/bin/python
DEBUG = False

import time
import socket
import pickle
import sys
import hashlib
from socket import *
from BlockChainDataStruct import *
from DataTransferFuns import *

m = hashlib.new('sha256')
m.update(b'bzvz')
ogledni = m.hexdigest()

def mine(transactions, prevHash):
    import hashlib
    import time
    import random


    difficultieLevel = 7
    targetString = "0000000"
    noviBlock = Block(transactions, prevHash)

    for i in range(6):
        print("#")
        print("razina tezine " + str(difficultieLevel))
        print("#")
        for j in range(3):
            noviBlock.nonce = 0
            guessNumber = 0

            flag = 1
            nonce = random.randrange(0, 5000000, 2)
            timerStart = time.time()

            while(flag):
                if(True):            
                    var = noviBlock.hashIt()
                    
                    hashPartForChacking = var[:difficultieLevel]
                    
                    if(hashPartForChacking == targetString):##hit done
                        flag = 0
                        timerEnd = time.time()
                        miningTime = timerEnd - timerStart
                        print(miningTime)

                        
                    else:                                   ##no hit, continue
                        guessNumber = guessNumber + 1
                        pass
                    
                nonce = nonce + 1
                noviBlock.nonce = nonce
        difficultieLevel = difficultieLevel + 1
        targetString = targetString+ "0"
            


def main():
    ideja1 = Transaction("Ante", "neki strifdsfsdfsang")
    ideja2 = Transaction("Ivo", "neki sdfdsfdsfdstring")
    ideja3 = Transaction("Marko", "nekigfdgdfsgdgdrg string")
    ideja4 = Transaction("Ante", "neki stringfsdfsdgfdsgsd")
    ideja5 = Transaction("Ivo", "neki 656464645string")
    ideja6 = Transaction("Marko", "neki strifdgrfgfggng")
    ideja7 = Transaction("Ante", "neki strfgdfgdfging")
    ideja8 = Transaction("Ivo", "neki strigfsgfsdgng")
    ideja9 = Transaction("Marko", "neki gsgdfsgsfgsgsstring")

    transactionQueue = [ideja1, ideja2,ideja3, ideja4, ideja5, ideja6, ideja7, ideja8, ideja9]
    hashPrevBlock = "1da64e1b2122c459934de1b6741f45cbf1d1b6f2ae6c1ff49bea166a60417a32"
    

    mine(transactionQueue, hashPrevBlock)

main()
    


