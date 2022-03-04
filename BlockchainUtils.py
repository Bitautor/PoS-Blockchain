from Crypto.Hash import SHA256
import json  # data could be any type so need json lib -> dumps()
import jsonpickle  # pickle: Python object serialization - convert a data structure into a linear form that can be stored or transmitted over a network


class BlockchainUtils:
    @staticmethod
    def hash(data):
        dataString = json.dumps(data)  # generate String from non structured data
        dataBytes = dataString.encode("utf-8")  # encode into byte representation
        dataHash = SHA256.new(dataBytes)  # SHA256 needs bytes / bytearray
        return dataHash

    @staticmethod
    def encode(object):
        # encode any object to send it through the p2p network
        return jsonpickle.encode(
            object, unpicklable=True
        )  # unpicklable=True to be able to recreate the object at receiver

    @staticmethod
    def decode(encodedObject):
        return jsonpickle.decode(encodedObject)
