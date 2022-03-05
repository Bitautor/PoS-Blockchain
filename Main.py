from Node import Node
import sys


if __name__ == "__main__":  # if program runs Main directly this is the entry point

    # sys.argv[0] = program
    ip = sys.argv[1]  # program start param1: ip address
    port = int(sys.argv[2])  # program start param2: p2p port number
    apiPort = int(sys.argv[3])  # program start param3: api port number

    node = Node(ip, port)
    node.startP2P()  # run peer-to-peer network communication
    node.startAPI(apiPort)  # run API for external communication
