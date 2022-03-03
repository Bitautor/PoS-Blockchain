from Crypto.Hash import SHA256
import json  # data could be any type so need json lib -> dumps()


class BlockchainUtils:
    @staticmethod
    def hash(data):
        dataString = json.dumps(data)  # generate String from non structured data
        dataBytes = dataString.encode("utf-8")  # encode into byte representation
        dataHash = SHA256.new(dataBytes)  # SHA256 needs bytes / bytearray
        return dataHash
