import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class NetworkGraph:
    def __init__(self):
        self.graph = nx.Graph()

    #グラフにノードを追加
    def add_node(self,node_id:int,label:str)->None:
        self.graph.add_node(node_id,label=label)
    #グラフにリンクを追加
    def add_link(self,node1_id,node2_id:int,label:str,bandwidth:int,delay:float)->None:
        self.graph.add_edge(node1_id,node2_id,label=label,bandwidth=bandwidth,delay=delay)

    #描画
    def draw(self):
        #self.graphに"bandwidth"の属性を追加<?>
        # リンクの帯域(bandwidth)によって線の太さを変える。
        def get_edge_width(bandwidth:int)->any:
            return np.log10(bandwidth) + 1  
        
        #self.graphに"delay"の属性を追加<?>
        #遅延(delay)の大きさによって線の色を変える。赤<黄色<緑
        def get_edge_color(delay:float)->str:
            if delay <= 0.001:
                return 'green'
            elif delay <= 0.01:
                return 'yellow'
            else:
                return 'red'
            
        #座標?各ノードの(x,y)が入る?、正負1.0が最大
        pos = nx.spring_layout(self.graph)
        #.edges()は各エッジの繋がりをタプルで返す。1<->2であれば、(1,2)。
        edge_widths = [get_edge_width(self.graph[u][v]['bandwidth']) for  u,v in self.graph.edges()]
        edge_colors = [get_edge_color(self.graph[u][v]['delay']) for u,v in self.graph.edges()]

        #with_labels:ノードの名前を表示。
        nx.draw(self.graph,pos,with_labels=False,node_color='lightblue',node_size=2000,width=edge_widths,edge_color=edge_colors)

        #deraw_networkx_labels()はパラメータで詳細を設定する関数
        #get_<>_attributes()はkeyの値を便利に取得
        nx.draw_networkx_labels(self.graph,pos,labels=nx.get_node_attributes(self.graph,"label"))
        nx.draw_networkx_edge_labels(self.graph,pos,labels=nx.get_edge_attributes(self.graph,"label"))

        plt.show()