from inspect import signature
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
import pprint

if __name__ == "__main__":  # if program runs Main directly this is the entry point

    # variables for testing reasons
    sender = "sender"
    receiver = "receiver"
    amount = 1
    type = "TRANSFER"

    wallet = Wallet()
    fraudulentWallet = Wallet()
    pool = TransactionPool()

    transaction = wallet.createTransaction(receiver, amount, type)

    if pool.transactionExists(transaction) == False:
        pool.addTransaction(transaction)

    block = wallet.createBlock(pool.transactions, 'lastHash', 1)
    signatureValid = Wallet.signatureValid(block.payload(), block.signature, wallet.publicKeyString())
    print(signatureValid)