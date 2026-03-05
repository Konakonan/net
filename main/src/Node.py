#型定義の文字列化
from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Link import Link   
    from Packet import Packet  

#Nodeクラスを作成
class Node:
    def __init__(
            self,
            node_id:int,
            address:str=None
            )->None:
        
        self.node_id = node_id
        self.address = address
        self.links = []
    
    #Linkの追加
    def add_link(self,link:Link)->None:
        if link not in self.links:
            self.links.append(link)

    #Packetの送信するメゾット
    def send_packet(self,packet:Packet)->None:
        if packet.destination == self.address:
            self.receive_packet(packet)
            print("b")
        
        else:
            for link in self.links:
                next_node = link.node_x if self != link.node_x else link.node_y
                print(f"ノード{self.node_id}からノード{next_node.node_id}へのパケット転送")
                link.transfer_packet(packet,self)
                break
        print("c")

        
    
    #Packetの受信するメゾット
    def receive_packet(self,packet:Packet)->None:
        print(f"ノード{self.node_id}がパケットを受信: {packet.payload}") 



     #返却   
    def __str__(self) -> str:
        #配列を展開、自身と同じNodeであれば、もう一方のNodeを取得。異なればそのまま取得。
        connected_nodes = [link.node_y.node_id if link.node_x == self else link.node_x.node_id for link in self.links]
        #配列を展開、文字列化して、カンマ区切りで結合。
        connected_nodes_str = ", ".join(str(node_id) for node_id in connected_nodes)    
        return f"ノード(ID:{self.node_id},アドレス:{self.address},接続:{connected_nodes_str})"
    


