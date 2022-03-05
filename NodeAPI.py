from crypt import methods
from urllib import response
from flask_classful import FlaskView, route
from flask import Flask, jsonify, request
from BlockchainUtils import BlockchainUtils

node = None  # constant for injected node


class NodeAPI(FlaskView):
    # NodeAPI: a FlaskView with endpoint API, creating routes
    # FlaskView creates endpoints to call via HTTP requests

    def __init__(self):
        # create Flask application (allows to interact with route endpoints)
        self.app = Flask(__name__)

    def start(self, apiPort):
        # registering app (Flask application) to NodeAPI
        # route_base: defines entry point for browser to generate HTTP request
        NodeAPI.register(self.app, route_base="/")
        self.app.run(host="localhost", port=apiPort)

    def injectNode(self, injectedNode):
        # inject node and use global variable to avoid problems with Flask initializer (=> not using self!)
        global node  # alter global variable 'node' from inside function
        node = injectedNode

    # use route decorator for navigation to endpoints
    # endpoint '/info'
    # only requesting information => methods: only 'GET', not 'POST'
    @route("/info", methods=["GET"])
    def info(self):
        # return test message
        return "This is the blockchain nodes API", 200  # 'OK' [Success]

    # endpoint '/blockchain'
    @route("/blockchain", methods=["GET"])
    def blockchain(self):
        # return json representation of blockchain
        return node.blockchain.toJson(), 200  # 'OK' [Success]

    # endpoint '/transactionPool'
    @route("/transactionPool", methods=["GET"])
    def transactionPool(self):
        transactions = {}
        for ctr, transaction in enumerate(node.transactionPool.transactions):
            transactions[ctr] = transaction.toJson()
        # jsonify: converts into json representation
        return jsonify(transactions), 200  # 'OK' [Success]

    # endpoint '/transaction'
    @route("/transaction", methods=["POST"])
    def transaction(self):
        # request: access data in the request, get_json: expect the data to be in json format (alternative: get_data)
        values = request.get_json()

        # check if data is transaction
        if not "transaction" in values:
            return "Missing transaction value", 400  # 'Bad Request' [Client Error]

        # decode transaction back to an object
        transaction = BlockchainUtils.decode(values["transaction"])

        # checking and adding transaction to the transaction pool
        node.handleTransaction(transaction)

        response = {"message": "Received transaction"}
        # return respronse message + code 201 (ndicates that the request has succeeded and a new resource has been created as a result.)
        return jsonify(response), 201  # 'Created' [Success]
