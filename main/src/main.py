from Node import Node
from Link import Link
from Packet import Packet
from NetworkGraph import NetworkGraph

def main():
    network_graph = NetworkGraph()
    node1 = Node(1,address="00:01",network_graph=network_graph)
    node2 = Node(2,address="00:02",network_graph=network_graph)
    #packet: Packet = Packet(source=node1.address,destination=node2.address,payload="Hello, World!")
    link = Link(node1,node2,network_graph=network_graph)
    print(node1)
    print(node2)
    #print(packet)
    print(link)
    #link.transfer_packet(packet,node2)

    #node1.send_packet(packet)
    network_graph.draw()

#実行
if __name__ == "__main__":
    main()