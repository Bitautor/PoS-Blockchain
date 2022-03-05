from Block import Block
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from ProofOfStake import ProofOfStake


class Blockchain:
    def __init__(self):
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()
        self.pos = ProofOfStake()

    def addBlock(self, block):
        self.executeTransactions(block.transactions)
        self.blocks.append(block)

    def toJson(self):
        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data["blocks"] = jsonBlocks
        return data

    def blockCountValid(self, block):
        if (
            self.blocks[-1].blockCount == block.blockCount - 1
        ):  # compare with latest block: blocks[-1]
            return True
        else:
            return False

    def lastBlockHashValid(self, block):
        latestBlockchainBlockHash = BlockchainUtils.hash(
            self.blocks[-1].payload()
        ).hexdigest()  # hexadecimal representation of hash of block payload
        if latestBlockchainBlockHash == block.lastHash:
            return True
        else:
            return False

    def getCoveredTransactionSet(self, transactions):
        coveredTransactions = []
        for transaction in transactions:
            if self.transactionCovered(transaction):
                coveredTransactions.append(transaction)
            else:
                print("Transaction is not covered by sender")
        return coveredTransactions

    def transactionCovered(self, transaction):
        if transaction.type == "EXCHANGE":
            # no checking if exchange transaction
            return True
        senderBalance = self.accountModel.getBalance(transaction.senderPublicKey)
        if senderBalance >= transaction.amount:
            return True
        else:
            return False

    def executeTransactions(self, transactions):
        for transaction in transactions:
            self.executeTransaction(transaction)

    def executeTransaction(self, transaction):
        if transaction == "STAKE":
            # special transaction to deposit a stake
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            # check if sender is equal to receiver because staking is only possible at the own wallet
            if sender == receiver:
                amount = transaction.amount  # amount of tokens to be staked
                self.pos.update(sender, amount)
                self.accountModel.updateBalance(sender, -amount)

        sender = transaction.senderPublicKey
        receiver = transaction.receiverPublicKey
        amount = transaction.amount
        # update senders balance
        self.accountModel.updateBalance(sender, -amount)
        # update receivers balance
        self.accountModel.updateBalance(receiver, amount)

    def nextForger(self):
        lastBlockHash = BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest()
        nextForger = self.pos.forger(lastBlockHash)
        return nextForger

    def createBlock(self, transactionsFromPool, forgerWallet):
        coveredTransactions = self.getCoveredTransactionSet(transactionsFromPool)
        self.executeTransactions(coveredTransactions)
        newBlock = forgerWallet.createBlock(
            coveredTransactions,
            BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest(),
            len(self.blocks),
        )
        self.blocks.append(newBlock)
        return newBlock

    def transactionExists(self, transaction):
        # iterate through the blockchain
        for block in self.blocks:
            for blockTransaction in block.transactions:
                if transaction.equals(blockTransaction):
                    # transaction already exists in the blockchain
                    return True
        return False  # new transaction - not in pool yet

    def forgerValid(self, block):
        # determine the next forger based on the state of own blockchain
        forgerPublicKey = self.pos.forger(block.lastHash)
        # compare with the proposed forger
        proposedBlockForger = block.forger
        if forgerPublicKey == proposedBlockForger:
            return True
        else:
            return False

    def transactionsValid(self, transactions):
        coveredTransactions = self.getCoveredTransactionSet(transactions)
        if len(coveredTransactions) == len(transactions):
            # there were no additional (fraudulent) transactions added
            return True
        else:
            return False
