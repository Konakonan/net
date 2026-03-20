#型定義の文字列化
from __future__ import annotations
from typing import TYPE_CHECKING 


if TYPE_CHECKING:
    from Node import Node
    from Packet import Packet

#Linkクラスの作成
class Link:
    def __init__(
            self,
            node_x:Node,
            node_y:Node,
            bandwideth:int=10000, #帯域幅
            delay:float=0.001, #遅延
            packet_loss:float=0.0 #パケットロス率
            )->None:
        
        self.node_x = node_x
        self.node_y = node_y
        self.bandwideth = bandwideth
        self.delay = delay
        self.packet_loss = packet_loss

        #リンクを追加
        node_x.add_link(self)
        node_y.add_link(self)
    
    #次のノードへパケットを渡すメゾット
    def transfer_packet(self,packet:Packet,from_node:Node)->None:
        next_node = self.node_x if from_node != self.node_x else self.node_y
        next_node.receive_packet(packet)

    #返却
    def __str__(self):
        return f"リンク({self.node_x.node_id} <-> {self.node_y.node_id}, 帯域幅:{self.bandwideth}, 遅延:{self.delay}, パケットロス率:{self.packet_loss})"
        