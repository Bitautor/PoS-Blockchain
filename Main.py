from Node import Node
import sys


if __name__ == "__main__":  # if program runs Main directly this is the entry point

    # sys.argv[0] = program
    ip = sys.argv[1]  # start param1: ip address
    port = int(sys.argv[2])  # start param2: p2p port number
    apiPort = int(sys.argv[3])  # start param3: api port number
    keyFile = None
    if len(sys.argv) > 4:
        keyFile = sys.argv[4]  # (optional) start param4: genesis PRIVATE KEY file

    node = Node(ip, port, keyFile)
    node.startP2P()  # run peer-to-peer network communication
    node.startAPI(apiPort)  # run API for external communication
