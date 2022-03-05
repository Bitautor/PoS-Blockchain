from BlockchainUtils import BlockchainUtils
from Message import Message
from TransactionPool import TransactionPool
from Wallet import Wallet
from Blockchain import Blockchain
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI


class Node:
    def __init__(self, ip, port):
        # api
        self.api = None
        # p2p communication
        self.p2p = None  # SocketCommunication: start communication via startP2P()
        self.ip = ip
        self.port = port
        # Blockchain + TransactionPool
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)

    def startAPI(self, apiPort):
        self.api = NodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)

    def handleTransaction(self, transaction):
        # checking transaction signature and if the transaction exists in transaction pool
        data = transaction.payload()
        signature = transaction.signature
        signerPublicKey = transaction.senderPublicKey
        signatureValid = Wallet.signatureValid(data, signature, signerPublicKey)
        transactionExists = self.transactionPool.transactionExists(transaction)
        if not transactionExists and signatureValid:
            # 1. add transaction to local transaction pool
            self.transactionPool.addTransaction(transaction)
            # 2. propagate transaction through the network via p2p message
            message = Message(self.p2p.socketConnector, "TRANSACTION", transaction)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)  # broadcast encoded transaction message
