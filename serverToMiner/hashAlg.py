import hashlib
import random

flag = 1
nonce = random.randrange(0, 500000, 2)
while(flag):
    if(True):

        m = hashlib.new('sha256')#.sha256()
        m.update(b"Nobody inspects")
        m.update(b" the spammish repetition")
        print(type(b"jajajaj"))
        m.update((str(nonce)).encode("utf-8"))
        
        var = m.hexdigest()
        print(var)
        

        
        provjera = var[:4]
        print("provjera" + provjera)
        if(provjera == "0000"):
            flag = 0
        print("provjera " + provjera)
        print(type(provjera))
        del m

    nonce = nonce + 1

