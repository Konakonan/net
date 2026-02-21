#型定義の文字列化
from __future__ import annotations


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
    def add_link(self,link)->None:
        if link not in self.links:
            self.links.append(link)

     #返却   
    def __str__(self):
        return f"ノード(ID:{self.node_id},アドレス:{self.address})"
    


