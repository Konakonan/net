#型定義の文字列化
from __future__ import annotations
#循環参照の回避
from typing import TYPE_CHECKING

from Link import Link
from Packet import Packet  
from NetworkGraph import NetworkGraph
from NetworkEventScheduler import NetworkEventSchaduler

if TYPE_CHECKING:
    from Link import Link   
    from Packet import Packet
    #from NetworkGraph import NetworkGraph


#Nodeクラスを作成
#デフォルト値無し↑、デフォルト値有り↓。
class Node:
    def __init__(
            self,
            node_id:int,#ID
            network_event_scheduler:NetworkEventSchaduler,
            address:str| None =None,#アドレス
            )->None:
        
        self.network_event_scheduler = network_event_scheduler
        self.node_id = node_id
        self.address = address
        #リンク先のアドレスを格納する配列
        self.links = []


        label = f"Node{node_id}/n{address}"
        #NetworkGraphを定義
        self.network_event_scheduler.add_node(node_id,label)

    
    #Linkの追加
    def add_link(self,link:Link)->None:
        if link not in self.links:
            self.links.append(link)

    #Packetの送信するメゾット
    def send_packet(self,packet:Packet)->None:
        #パケット送信をログに記録
        self.network_event_scheduler.log_packet_info(packet,"sent",self.node_id)
        #宛先が自身の場合は受信処理
        if packet.header["destination"] == self.address:
            self.receive_packet(packet)
        
        else:
            for link in self.links:
                next_node = link.node_x if self != link.node_x else link.node_y
                print(f"ノード{self.node_id}からノード{next_node.node_id}へのパケット転送")
                #リンクを通じてパケットを送信
                link.enqueue_packet(packet,self)
                #ループを抜ける
                break

        
    
    #Packetの受信するメゾット
    def receive_packet(self,packet:Packet)->None:
        #パケットが失われた場合
        if packet.arrival_time == -1:
            self.network_event_scheduler.log_packet_info(packet,"lost",self.node_id)
            return
        #パケットが到着した場合
        if packet.header["destination"] == self.address:
            #パケット到着をログに記録
            self.network_event_scheduler.log_packet_info(packet,"arrived",self.node_id)
            #到着時刻を設定
            packet.set_arrived(self.network_event_scheduler.current_time)

        else:
            #パケットの受信をログに記録
            self.network_event_scheduler.log_packet_info(packet,"received",self.node_id) 

    #パケットを生成するメゾット
    def crent_packet(self,destination,header_size,payload_size):
        packet = Packet(source=self.address, destination=destination, header_size=header_size, payload_size=payload_size,network_event_scheduler=self.network_event_scheduler)
        self.network_event_scheduler.log_packet_info(packet,"created",self,self.node_id)
        self.send_packet(packet)

    #トラフィックを設定するメゾット
    def set_traffic(self, destination, bitrate, start_time, duration, header_size, payload_size,burstiness=1.0):
        #トラフィックの終了時刻
        end_time = start_time + duration
        def generate_packet():
            if self.network_event_scheduler.current_time < end_time:
                #パケットを生成して送信
                self.crent_packet(destination, header_size, payload_size)

                packet_size = header_size + payload_size
                #次のパケットを生成するまでの間隔
                interval = (packet_size *8) /bitrate * burstiness
                self.network_event_scheduler.schedule_event(self.network_event_scheduler.current_time + interval, generate_packet)
            
        #最初のパケット生成イベントをスケジュール
        self.network_event_scheduler.schedule_event(start_time,generate_packet)



     #返却   
    def __str__(self) -> str:
        #配列を展開、自身と同じNodeであれば、もう一方のNodeを取得。異なればそのまま取得。
        connected_nodes = [link.node_y.node_id if link.node_x == self else link.node_x.node_id for link in self.links]
        #配列を展開、文字列化して、カンマ区切りで結合。
        connected_nodes_str = ", ".join(str(node_id) for node_id in connected_nodes)    
        return f"ノード(ID:{self.node_id},アドレス:{self.address},接続:{connected_nodes_str})"
    


