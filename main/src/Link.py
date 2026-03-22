#型定義の文字列化
from __future__ import annotations
from typing import TYPE_CHECKING 
from NetworkGraph import NetworkGraph


if TYPE_CHECKING:
    from Node import Node
    from Packet import Packet
    from NetworkGraph import NetworkGraph

#Linkクラスの作成
class Link:
    def __init__(
            self,
            node_x:Node,
            node_y:Node,
            network_graph:NetworkGraph,
            bandwidth:int=10000, #帯域幅
            delay:float=0.001, #遅延
            packet_loss:float=0.0 #パケットロス率
            )->None:
        
        self.node_x = node_x
        self.node_y = node_y
        self.bandwidth = bandwidth
        self.delay = delay
        self.packet_loss = packet_loss
        #NetworkGraphを定義
        self.network_graph = network_graph

        #グラフにリンクを追加
        label = f"{bandwidth/1000000}Mbps,{delay}s"
        self.network_graph.add_link(node_x.node_id,node_y.node_id,label,self.bandwidth,self.delay)

        #リンクを追加
        node_x.add_link(self)
        node_y.add_link(self)
    
    #次のノードへパケットを渡すメゾット
    def transfer_packet(self,packet:Packet,from_node:Node)->None:
        next_node = self.node_x if from_node != self.node_x else self.node_y
        next_node.receive_packet(packet)

    #返却
    def __str__(self):
        return f"リンク({self.node_x.node_id} <-> {self.node_y.node_id}, 帯域幅:{self.bandwidth}, 遅延:{self.delay}, パケットロス率:{self.packet_loss})"
        