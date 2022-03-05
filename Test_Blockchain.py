from Wallet import Wallet
from TransactionPool import TransactionPool
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
import pprint


# TESTING: interaction with Blockchain (create transaction, create block, manage transaction pool)

if __name__ == "__main__":  # ENTRY POINT

    blockchain = Blockchain()
    pool = TransactionPool()

    alice = Wallet()
    bob = Wallet()
    exchange = Wallet()
    forger = Wallet()

    exchangeTransaction = exchange.createTransaction(
        alice.publicKeyString(), 10, "EXCHANGE"
    )

    if not pool.transactionExists(exchangeTransaction):
        pool.addTransaction(exchangeTransaction)

    coveredTransactions = blockchain.getCoveredTransactionSet(pool.transactions)
    lastHash = BlockchainUtils.hash(blockchain.blocks[-1].payload()).hexdigest()
    blockCount = blockchain.blocks[-1].blockCount + 1
    blockOne = forger.createBlock(coveredTransactions, lastHash, blockCount)
    blockchain.addBlock(blockOne)
    pool.removeFromPool(blockOne.transactions)

    # alice wants to send 5 tokens to bob
    transaction = alice.createTransaction(bob.publicKeyString(), 5, "TRANSFER")

    if not pool.transactionExists(transaction):
        pool.addTransaction(transaction)

    coveredTransactions = blockchain.getCoveredTransactionSet(pool.transactions)
    lastHash = BlockchainUtils.hash(blockchain.blocks[-1].payload()).hexdigest()
    blockCount = blockchain.blocks[-1].blockCount + 1
    blockTwo = forger.createBlock(coveredTransactions, lastHash, blockCount)
    blockchain.addBlock(blockTwo)
    pool.removeFromPool(blockTwo.transactions)

    pprint.pprint(blockchain.toJson())
