from math import fabs
import threading
import time
from Message import Message
from BlockchainUtils import BlockchainUtils


class PeerDiscoveryHandler:
    def __init__(self, node):
        self.socketCommunication = node

    def start(self):
        # start status() and discovery() in own threads
        # new Thread: target=method, no args
        statusThread = threading.Thread(target=self.status, args=())
        statusThread.start()
        discoveryThread = threading.Thread(target=self.discovery, args=())
        discoveryThread.start()

    def status(self):
        while True:
            # print out current connections
            print("Current connections:")
            for peer in self.socketCommunication.peers:
                print(str(peer.ip) + ":" + str(peer.port))
            time.sleep(10)

    def discovery(self):
        while True:
            # broadcast handshake message
            handshakeMessage = self.handshakeMessage()
            self.socketCommunication.broadcast(handshakeMessage)
            time.sleep(10)

    def handshake(self, connect_node):
        # exchange of information between two nodes
        handshakeMessage = self.handshakeMessage()
        self.socketCommunication.send(connect_node, handshakeMessage)

    def handshakeMessage(self):
        # send the known peers to the new connected node
        ownConnector = self.socketCommunication.socketConnector
        ownPeers = self.socketCommunication.peers
        data = ownPeers  # message content: peers (list of known nodes)
        messageType = "DISCOVERY"
        message = Message(ownConnector, messageType, data)
        encodedMessage = BlockchainUtils.encode(message)  # serialize object to send it
        return encodedMessage

    def handleMessage(self, message):
        # avoid adding multiple instances of a peer already added
        peersSocketConnector = message.senderConnector
        peersPeerList = message.data  # list of peers the sender knows

        # check for each peer in own peer list if the senderConnector exists
        newPeer = True
        for peer in self.socketCommunication.peers:
            if peer.equals(peersSocketConnector):
                newPeer = False
        if newPeer == True:
            self.socketCommunication.peers.append(peersSocketConnector)

        # check for each peer in own peer list if the specific peer from peersPeerList exists
        for peersPeer in peersPeerList:
            peerKnown = False
            for peer in self.socketCommunication.peers:
                if peer.equals(peersPeer):
                    peerKnown = True
            if not peerKnown and not peersPeer.equals(
                self.socketCommunication.socketConnector
            ):
                # new peer is NOT known AND NOT the own socket
                self.socketCommunication.connect_with_node(peersPeer.ip, peersPeer.port)
