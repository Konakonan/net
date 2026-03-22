import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import heapq
#key無しでも自動生成
from collections import defaultdict

class NetworkEventSchaduler:

    def __init__(self,log_enabled:bool=False,verbose:bool=False)->None:
        self.current_time:int = 0 #
        self.events:list = [] #
        self.event_id:int = 0 #
        self.packet_logs = {} 
        self.log_enabled = log_enabled #
        self.verbose = verbose #
        self.graph = nx.Graph()


    def add_node(self,node_id,label):
        self.graph.add_node(node_id,label=label)
    
    def add_link(self,node1_id,node2_id:int,label:str,bandwidth:int,delay:float)->None:
        self.graph.add_edge(node1_id,node2_id,label=label,bandwidth=bandwidth,delay=delay)

    
     #描画
    def draw(self):
        def get_edge_width(bandwidth:int)->any:
            return np.log10(bandwidth) + 1  
        
        def get_edge_color(delay:float)->str:
            if delay <= 0.001:
                return 'green'
            elif delay <= 0.01:
                return 'yellow'
            else:
                return 'red'
            
        pos = nx.spring_layout(self.graph)
        edge_widths = [get_edge_width(self.graph[u][v]['bandwidth']) for  u,v in self.graph.edges()]
        edge_colors = [get_edge_color(self.graph[u][v]['delay']) for u,v in self.graph.edges()]

        nx.draw(self.graph,pos,with_labels=False,node_color='lightblue',node_size=2000,width=edge_widths,edge_color=edge_colors)

        nx.draw_networkx_labels(self.graph,pos,labels=nx.get_node_attributes(self.graph,"label"))
        nx.draw_networkx_edge_labels(self.graph,pos,labels=nx.get_edge_attributes(self.graph,"label"))

        plt.show()

    
    def schedule_event(self,event_time,callback,*args):
        event = (event_time,self.event_id,callback,args)
        heapq.heappush(self.events,event)
        self.evvent_id += 1


    def log_packet_infor(self,packet,event_type,node_id=None):
        if self.log_enabled:
            if packet.id not in self.packet_logs:
                self.packet_logs[packet.id] = {
                    "source" : packet.header["source"],
                    "destination" : packet.header["destination"],
                    "size" : packet.size,
                    "creation_time" : packet.creation_time,
                    "arrival_time" : packet.arrival_time,
                    "events" : [],
                }


            if event_type == "arrived":
                self.packet_logs["packet_id"]["arrival_time"] = self.current_time

            event_info = {
                "time" : self.current_time,
                "event" : event_type,
                "node_id" : node_id,
                "packet_id" : packet.id,
                "src" : packet.header["source"],
                "dst" : packet.header["destination"],
            }
            self.packet_logs[packet.id]["events"].append(event_info)


            if self.verbose:
                print(f"Time:{self.current_time},Node:{node_id},Event:{event_type},Packet:{packet.id},Src:{packet.header["source"]},Dst:{packet.header["destination"]}")


    def print_packet_logs(slef):
        pass

    def generate_summary(self,packet_logs):
        summary_date = defaultdict(lambda: {"sent_packets":0,
                                            "sent_bytes":0,
                                            "recevied_packets":0,
                                            "recevied_bytes":0,
                                            "total_delay":0,
                                            "lost_packets":0,
                                            "mine_creation_time":float("inf"),
                                            "max_arrival_time":0
                                            })
    def generate_throughput_grapg(self):
        pass
    def generate_delay_histogram(self):
        pass

    def run(self):
        pass

    def run_util(self):
        pass


