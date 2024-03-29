import copy
from operator import ge
import time


class Block:
    def __init__(
        self, transactions, lastHash, forger, blockCount
    ):  # forger: miners public key string, blockCount: inkrementing number as the blockchain grows
        self.transactions = transactions
        self.lastHash = lastHash
        self.forger = forger
        self.blockCount = blockCount
        self.timestamp = time.time()
        self.signature = ""

    # generate first block in blockchain
    @staticmethod
    def genesis():
        genesisBlock = Block([], 'genesisHash', 'genesis', 0)
        genesisBlock.timestamp = 0 # hardcoded timestamp: the blockchain state of another node wouldn't accepted because of different genesis block timestamps => different lastHash values
        return genesisBlock

    def toJson(self):
        # generate output string manually (not using __dict__ here, because we want to output the whole transactions list)
        data = {}
        data["lastHash"] = self.lastHash
        data["forger"] = self.forger
        data["blockCount"] = self.blockCount
        data["timestamp"] = self.timestamp
        data["signature"] = self.signature
        jsonTransactions = []
        for transaction in self.transactions:
            jsonTransactions.append(transaction.toJson())
        data["transactions"] = jsonTransactions
        return data

    def sign(self, signature):
        self.signature = signature

    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation["signature"] = ""
        return jsonRepresentation
