from Block import Block
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel


class Blockchain:
    def __init__(self):
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()

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
                print("Transaction is not covered bei sender")
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
        sender = transaction.senderPublicKey
        receiver = transaction.receiverPublicKey
        amount = transaction.amount
        # update senders balance
        self.accountModel.updateBalance(sender, -amount)
        # update receivers balance
        self.accountModel.updateBalance(receiver, amount)