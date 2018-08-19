#!/usr/bin/python
DEBUG = False

import hashlib
import pickle

class Transaction:
    def __init__(self, creator, idea):
        self.creator = creator
        self.idea = idea
    def __repr__(self):
        return str("Ideja: " + self.idea + ", autor: " + self.creator + ".\n")
    def dataType(self):
        return "transaction"


class Block:
    def __init__(self, transactions, hashPrevBlock):
        self.transactions = transactions
        self.hashPrevBlock = hashPrevBlock
        self.nonce = None
    def display(self):
        print("#####################################################")
        print("Hash of prev block: ")
        print(self.hashPrevBlock)
        print("Hash of this block: ")
        print(self.hashIt())
        for transaction in self.transactions:
            print(transaction)
        print("#####################################################")
    def dataType(self):
        return "block"
    def hashIt(self):
        m = hashlib.new('sha256')
        m.update(pickle.dumps(self))
        tmp = m.hexdigest()
        del m
        return tmp
