#Nodeクラスを作成
class Node:
    def __init__(self,node_id,address=None):
        self.node_id = node_id
        self.address = address
        self.links = []
    
    def __str__(self):
        return f"ノード(ID:{self.node_id},アドレス:{self.address})"

