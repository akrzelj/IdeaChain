import hashlib
import time
import random

difficultieLevel = 6
targetString = "000000"

for i in range(1):##we will measure 5 difficultie levels
    nazivFajla = "UKUPNmjerenjaVreman" + str(difficultieLevel) + ".txt"
    f = open(nazivFajla, "w")

    for j in range(5):##we mine 5 times every difficultie level
        ##f.write("ulaz u drugi for\n")
        flag = 1
        nonce = random.randrange(0, 500000, 2)
        timeStart = time.time()
        guessNumber = 0
        while(flag):
            if(True):
                m = hashlib.new('sha256')
                m.update(b"kreator nove ideje")
                m.update(b" njegova velika mudrost")
                m.update((str(nonce)).encode("utf-8"))
                print("di pusas")
                
                var = m.hexdigest()
                
                hashPartForChacking = var[:difficultieLevel]
                print(hashPartForChacking)
                
                if(hashPartForChacking == targetString):##hit done
                    flag = 0
                    timeElapsed = time.time() - timeStart
                    infoString = "Mining of block with difficultie level: " + str(difficultieLevel) + " took " + str(timeElapsed) + " seconds and " + str(guessNumber) + " of repeation.\n"
                    f.write(infoString)
                    
                else:                                   ##no hit, continue
                    guessNumber = guessNumber + 1
                    pass
                
                del m
            nonce = nonce + 1
   
    difficultieLevel = difficultieLevel + 1
    targetString = targetString + "0"

    f.close()
