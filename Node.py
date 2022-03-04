from TransactionPool import TransactionPool
from Wallet import Wallet
from Blockchain import Blockchain
from SocketCommunication import SocketCommunication


class Node:
    def __init__(self, ip, port):
        # p2p communication
        self.p2p = None  # start communication via startP2P() not initially
        self.ip = ip
        self.port = port
        # Blockchain + TransactionPool
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication()
