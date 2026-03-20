from Node import Node
from Link import Link
from Packet import Packet
 

def main():
    node1 = Node(1,address="00:01")
    node2 = Node(2,address="00:02")
    packet: Packet = Packet(source=node1.address,destination=node2.address,payload="Hello, World!")
    link = Link(node1,node2)
    print(node1)
    print(node2)
    print(packet)
    print(link)
    #link.transfer_packet(packet,node2)

    node1.send_packet(packet)


#実行
if __name__ == "__main__":
    main()