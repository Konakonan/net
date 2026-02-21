#型定義の文字列化
from __future__ import annotations
from Node import Node

#Linkクラスの作成
class Link:
    def __init__(
            self,
            node_x:Node,
            node_y:Node,
            bandwideth:int=10000,
            delay:float=0.001,
            packet_loss:float=0.0
            )->None:
        
        self.node_x = node_x
        self.node_y = node_y
        self.bandwideth = bandwideth
        self.delay = delay
        self.packet_loss = packet_loss
    
    #返却
    def __str__(self):
        return f"リンク({self.node_x.node_id} <-> {self.node_y.node_id}, 帯域幅:{self.bandwideth}, 遅延:{self.delay}, パケットロス率:{self.packet_loss})"
        