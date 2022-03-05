from inspect import signature
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5  # generate and validate signatures
from BlockchainUtils import BlockchainUtils  # create key pair
from Transaction import Transaction
from Block import Block


class Wallet:
    def __init__(self):
        self.keyPair = RSA.generate(2048)

    def fromKey(self, file):
        # reading key from file
        key = ""
        with open(file, "r") as keyfile:
            # import RSA key from file
            key = RSA.import_key(keyfile.read())
        self.keyPair = key

    def sign(self, data):  # creates signature of the key pair and its own data
        dataHash = BlockchainUtils.hash(data)
        signatureSchemeObject = PKCS1_v1_5.new(
            self.keyPair
        )  # create sig scheme obj (based on RSA key pair) to generate and validate sigs
        signature = signatureSchemeObject.sign(
            dataHash
        )  # create signature from data hash
        return signature.hex()

    @staticmethod
    def signatureValid(
        data, signature, publicKeyString
    ):  # publicKeyString used to initially sign the data in string format
        signature = bytes.fromhex(signature)  # convert hex string back to byte obj
        dataHash = BlockchainUtils.hash(data)  # hash same input data
        publicKey = RSA.importKey(publicKeyString)
        signatureSchemeObject = PKCS1_v1_5.new(
            publicKey
        )  # only need public key for signature validation -> verify()
        signatureValid = signatureSchemeObject.verify(
            dataHash, signature
        )  # checks if signature corresponds to dataHash based on public key
        return signatureValid

    def publicKeyString(self):
        ## RSA export keys:
        # keys.exportKey() for the private key
        # keys.publickey().exportKey() for the public key
        ## PEM:
        # Privacy Enhanced Mail is a Base64 encoded DER certificate (digital certificate in binary format)
        ## Python string encode() function / Python bytes decode() function
        # encode: string obj -> bytes obj (immutable sequence of integers in the range 0 <= x < 256) [“utf-8” encoding is used as default]
        # decode: bytes obj -> string obj
        publicKeyString = (
            self.keyPair.publickey().exportKey("PEM").decode("utf-8")
        )  # RSA public key obj -> bytes obj -> string obj
        return publicKeyString

    # create and sign new transaction
    def createTransaction(
        self, receiver, amount, type
    ):  # sender is always the same - wallet owner
        transaction = Transaction(self.publicKeyString(), receiver, amount, type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction

    # create and sign new block
    def createBlock(self, transactions, lastHash, blockCount):
        block = Block(transactions, lastHash, self.publicKeyString(), blockCount)
        signature = self.sign(block.payload())
        block.sign(signature)
        return block
