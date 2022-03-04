from p2pnetwork.node import Node  # import Node class to create p2p connections
from PeerDiscoveryHandler import PeerDiscoveryHandler
from SocketConnector import SocketConnector
from BlockchainUtils import BlockchainUtils
import json


class SocketCommunication(Node):

    # p2p communication via ip address and port -> socket communication
    # SocketCommunication class is a subclass of Node
    # Node class is able to connect to other sockets within the network and communicate with them

    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port)
        self.peers = []
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)
        self.socketConnector = SocketConnector(ip, port)

    def connectToFirstNode(self):
        if self.socketConnector.port != 10001:
            # this node is NOT the INITIAL NODE (first node in the network)
            self.connect_with_node("localhost", 10001)  # CONNECT WITH OTHER NODE

    def startSocketCommunication(self):
        # open port for socket communication
        self.start()  # start self (p2p node) as socket communication
        self.peerDiscoveryHandler.start()  # start PeerDiscoveryHandler -> 2 Threads
        self.connectToFirstNode()

    # connection listeners (callback methods)

    def inbound_node_connected(self, connected_node):
        # other node connected to this node
        # -> handshake with connected node
        self.peerDiscoveryHandler.handshake(connected_node)

    def outbound_node_connected(self, connected_node):
        # this node connects to other node
        # -> handshake with connected node
        self.peerDiscoveryHandler.handshake(connected_node)

    def node_message(self, connected_node, message):
        message = BlockchainUtils.decode(json.dumps(message))
        if message.messageType == 'DISCOVERY':
            self.peerDiscoveryHandler.handleMessage(message)

    def send(self, receiver, message):
        # interface for sending message to a node
        self.send_to_node(receiver, message)

    def broadcast(self, message):
        # interface for broadcasting message to all nodes
        self.send_to_nodes(message)
