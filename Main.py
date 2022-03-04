from Node import Node
import sys

if __name__ == "__main__":  # if program runs Main directly this is the entry point

    ip = sys.argv[1] # program start param1 (param0 = program)
    port = int(sys.argv[2]) # program start param2

    node = Node(ip, port)
    node.startP2P()