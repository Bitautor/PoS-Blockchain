class TransactionPool:
    def __init__(self):
        self.transactions = []

    def addTransaction(self, transaction):
        self.transactions.append(transaction)

    def transactionExists(self, transaction):
        # check if this transaction exists
        for trx in self.transactions:
            if trx.equals(transaction):
                return True
        return False

    def removeFromPool(self, transactions):
        newPoolTransactions = []
        for poolTransaction in self.transactions:
            insert = True
            for transaction in transactions:
                if poolTransaction.equals(transaction):
                    insert = False
            if insert == True:
                newPoolTransactions.append(poolTransaction)
        self.transactions = newPoolTransactions