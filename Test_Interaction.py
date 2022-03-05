from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests  # HTTP library


# TESTING: interaction with Blockchain API (-> sending HTTP requests using requests lib)

if __name__ == "__main__":  # ENTRY POINT

    bob = Wallet()
    alice = Wallet()
    exchange = Wallet()

    transaction = exchange.createTransaction(alice.publicKeyString(), 10, "EXCHANGE")

    url = "http://localhost:5000/transaction"
    # provide data in json format (-> request.get_json() in NodeAPI.transactiBlockchainUtils.encode(transaction)
    package = {"transaction": BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)
    print(request.text)
