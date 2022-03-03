from inspect import signature
import uuid  # global unique id lib
import time  # timestamp lib
import copy


class Transaction:
    def __init__(self, senderPublicKey, receiverPublicKey, amount, type):
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = receiverPublicKey
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ""  # sign transaction with your own private key

    def toJson(self):
        return (
            self.__dict__
        )  # contains all the attributes which describe the object (__dict__ can be used to alter or read the attributes)

    def sign(self, signature):
        self.signature = signature

    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation["signature"] = ""
        return jsonRepresentation  # contains the transaction data without signature to compare while validating the transaction

    def equals(self, transaction):
        if self.id == transaction.id:
            return True
        else:
            return False
