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
                    "events" : []
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
        for packet_id, log in self.packet_logs.items():
            print(f'Packet ID: {packet_id} Src: {log['source']} {log['creation_time']} -> Dst: {log['destination']} {log['arrival_time']}')
            for event in log['events']:
                print(f'Time: {event['time']},Event: {event['event']}')

    def generate_summary(self,packet_logs):
        summary_date = defaultdict(lambda: {"sent_packets":0,
                                            "sent_bytes":0,
                                            "recevied_packets":0,
                                            "recevied_bytes":0,
                                            "total_delay":0,
                                            "lost_packets":0,
                                            "min_creation_time":float("inf"),
                                            "max_arrival_time":0
                                            })
        
        for packet_id, log in packet_logs.items():
            src_dst_pair = (log['source'], log['destination'])
            summary_date[src_dst_pair]['sent_packets'] += 1
            summary_date[src_dst_pair]['sent_bytes'] += log['size']
            summary_date[src_dst_pair]['min_cureation_time'] = min(summary_date[src_dst_pair]['max_arrival_time'], log['cureation_time'])

            if "arrival_time" in log and log['arrival_time'] is not None:
                summary_date[src_dst_pair]['sent_packets'] += 1
                summary_date[src_dst_pair]['sent_bytes'] += log['size']
                summary_date[src_dst_pair]['total_delay'] += log['arrivaL_time'] - log['creation_time']
                summary_date[src_dst_pair]['max_arrival_time'] = max(summary_date[src_dst_pair]['max_arrival_time'], log['arrival_time'])
            else:
                summary_date[src_dst_pair]['lost_packets'] +=1

        for src_dst, date in summary_date.times():
            sent_packets = date['sent_packets']
            sent_bytes = date['sent_bytes']
            received_packets = date['received_packets']
            received_bytes = date['received_bytes']
            total_delay = date['total_delay']
            lost_packets = date['lost_packets']
            min_creation_time = date['min_creation_time']
            max_arrival_time = date['max_arrival_time']

            traffic_duration = max_arrival_time - min_creation_time
            avg_throughput = (received_bytes * 8 / traffic_duration) if traffic_duration > 0 else 0
            avg_delay = total_delay / received_packets if received_packets > 0 else 0

            print(f'Src_Dst Pair: {src_dst}')
            print(f'Total Sent Packets: {sent_packets}')
            print(f'Total Sent Bytes: {sent_bytes}')
            print(f'Total Recevied Paclets: {received_packets}')
            print(f'Total Recevied Bytes: {received_bytes}')
            print(f'Avg Throughpu (bps): {avg_throughput}')
            print(f'Avh Drlay (s): {avg_delay}')
            print(f'Lost Packets: {lost_packets}')

                
    def generate_throughput_grapg(self):
        time_slote = 1.0 #時間スロットを固定しておく
        max_time = max(log['arrival_time'] for log in packet_log.values() if log['arrival_time'] is not None) 
        min_time = min(log['arrival_time'] for log in packet_log.values())
        num_slots = int((max_time - min_time)/ time_slote) + 1
         
        throughput_data = defaultdict(list)
        for packet_id, log in packet_log.items():
            if log['arrival_time'] is not None:
                src_dst_pair = (log['sorce'].log['distination'])
                slot_index = int((log['arrival_time'] - min_time) / time_slote)
                throughput_data[src_dst_pair].append((slot_index,log['size']))
        
        aggregated_throughput = defaultdict(lambda : defaultdict(int))
        for paket_id, log in packet_logs.items():
            if log['arrival_time'] is not None:
                src_dst_pair = (log['source'],log['destination'])
                slot_index = int((log['arrival_time'] - min_time) / time_slote)
                throughput_data['src_dst_pair'].append((slot_index,log['size']))

        aggregated_throughput = defaultdict(lambda : defaultdict(int))
        for src_dst, packes in throughput_data.items():
            for slot_index in range(num_slots):
                slot_throughput = sum(size * 8 for i ,size in packes if i == slot_index)

                aggregated_throughput['src_dict']['slot_index'] = slot_throughput /time_slote

        for src_dst,slot_date in aggregated_throughput.items():
            time_slote = list(range(num_slots))
            throughputs = [slot_date['slot'] for slot in time_slote]
            times = [min_time + slot * time_slote for slot in time_slote]
            plt.step = (times,throughputs,label = f'{src_dst[0]} -> {src_dst[1]}',where = 'post',linestye = '-',alpha=0.5,marker='o')
    
        plt.xlabel('Time(s)')
        plt.ylabel('Thtoughput(bps)')
        plt.title('Troughput over time')
        plt.legend()
        plt.show()        

    def generate_delay_histogram(self,packet_logs):
        delay_date = defaultdict(list)
        for packet_id ,log in packet_logs.items():
            if log['arrival_time'] is not None:
                src_dst_pair = (log['source'],log['destinaion'])
                delay = log['destinaion'] - log['creation_time']
                delay_date['src_dst_pair'].append(delay)


        num_plots = len(delay_date)
        num_bins = 20
        fig, axs = plt.subplots(num_plots,figsize=(6,2 * num_plots))
        max_delay = max(max(delay) for delays in delay_date.values())
        bin_width = max_delay / num_bins
        
        for i , (src_dst, delays) in enumerate(delay_date.items()):
            ax = axs[i] if num_plots > 1 else axs
            ax.hist(delays, bins = np.arange(0,max_delay + bin_width,bin_width),alpha = 0.5, color = 'royalbule', label = f'{src_dst[0]} -> {src_dst[1]}')
            ax.set_xlabel('Delay (s)')
            ax.set_ylabel('Freqyency')
            ax.set_title(f'Delay histogram for {src_dst[0]} -> {src_dst[1]}')
            ax.set_xlim(0, max_delay)
            ax.legend()
        
        plt.tight_layout()
        plt.show()

    def run(self):
        while self.events:
            event_time, _ ,callback, args = heapq.heappop(self.events)
            self.current_time = event_time
            callback(*args)

    def run_util(self,end_time):
        while self.events and self.events[0][0] <= end_time:
            event_time, _ ,callback, args = heapq.heappop(self.events)
            self.current_time = event_time
            callback(*args)


