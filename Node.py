from BlockchainUtils import BlockchainUtils
from Message import Message
from TransactionPool import TransactionPool
from Wallet import Wallet
from Blockchain import Blockchain
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI
import copy


class Node:
    def __init__(self, ip, port, key=None):
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
        if key is not None:
            # create nodes based on serialized pem key files
            self.wallet.fromKey(key)

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)

    def startAPI(self, apiPort):
        self.api = NodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)

    def handleTransaction(self, transaction):
        # checking transaction signature (A) and if the transaction exists in transaction pool (B) or in the blockchain

        # (A) check if signature is valid
        data = transaction.payload()
        signature = transaction.signature
        signerPublicKey = transaction.senderPublicKey
        signatureValid = Wallet.signatureValid(data, signature, signerPublicKey)

        # (B) check if transaction is already in the transaction pool
        transactionExistsInPool = self.transactionPool.transactionExists(transaction)

        # (C) check if transaction is already in the blockchain
        transactionExistsInBlockchain = self.blockchain.transactionExists(transaction)

        if (
            signatureValid
            and not transactionExistsInPool
            and not transactionExistsInBlockchain
        ):
            # 1. ADD transaction to local transaction pool
            self.transactionPool.addTransaction(transaction)
            # 2. PROPAGATE transaction through the network via p2p message
            message = Message(self.p2p.socketConnector, "TRANSACTION", transaction)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)  # broadcast encoded transaction message
            # 3. FORGING required check - whether to generate new block or not
            forgingRequired = self.transactionPool.forgingRequired()
            if forgingRequired:
                self.forge()

    def handleBlock(self, block):

        # check if signature is valid
        blockData = block.payload()
        signature = block.signature
        forger = block.forger
        signatureValid = Wallet.signatureValid(blockData, signature, forger)

        # check if blockCount and lastBlockHash is valid
        blockCountValid = self.blockchain.blockCountValid(block)
        lastBlockHashValid = self.blockchain.lastBlockHashValid(block)

        # check if forger is valid
        forgerValid = self.blockchain.forgerValid(block)

        # check if transactions are valid
        transactionsValid = self.blockchain.transactionsValid(block.transactions)

        # special treatment if blockCount is not valid
        if not blockCountValid:
            # request other nodes for valid blockchain state
            self.requestChain()

        if signatureValid and lastBlockHashValid and forgerValid and transactionsValid:
            # everything is valid => adding block to local blockchain instance, remove block transactions from local pool instance
            self.blockchain.addBlock(block)
            self.transactionPool.removeFromPool(block.transactions)
            # forward message to all peers -> broadcast this block
            message = Message(self.p2p.socketConnector, "BLOCK", block)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)

    def requestChain(self):
        # creating message and broadcast the network
        message = Message(self.p2p.socketConnector, "BLOCKCHAIN_REQUEST", None)
        encodedMessage = BlockchainUtils.encode(message)
        self.p2p.broadcast(encodedMessage)

    def handleBlockchainRequest(self, requestingNode):
        message = Message(self.p2p.socketConnector, "BLOCKCHAIN_RESPONSE", self.blockchain)
        encodedMessage = BlockchainUtils.encode(message)
        self.p2p.send(requestingNode, encodedMessage)

    def handleBlockchain(self, blockchain):
        # append blocks (if valid) from received blockchain if newer than the latest blocks in local blockchain
        localBlockchainCopy = copy.deepcopy(self.blockchain)
        localBlockCount = len(localBlockchainCopy.blocks)
        receivedBlockCount = len(blockchain.blocks)
        if localBlockCount < receivedBlockCount:
            # received blockchain is in a newer state than the local blockchain representation
            for blockNumber, block in enumerate(blockchain.blocks):
                if blockNumber >= localBlockCount:
                    # add this block from received blockchain to local blockchain
                    localBlockchainCopy.addBlock(block)
                    self.transactionPool.removeFromPool(block.transactions)
            self.blockchain = localBlockchainCopy

    def forge(self):
        # get next forger and do forging
        forger = self.blockchain.nextForger()
        if forger == self.wallet.publicKeyString():
            # current wallet is the next FORGER
            print("next forger wallet")
            # create new block and add to local blockchain instance
            block = self.blockchain.createBlock(
                self.transactionPool.transactions, self.wallet
            )
            # remove transactions from local transaction pool instance
            self.transactionPool.removeFromPool(block.transactions)
            # broadcast new block to the network of nodes
            message = Message(self.p2p.socketConnector, "BLOCK", block)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)
        else:
            # current wallet is NOT the next forger
            print("not the next forger")
