#型定義の文字列化
from __future__ import annotations
from typing import TYPE_CHECKING 
from NetworkGraph import NetworkGraph
import heapq
import random


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
            loss_rate, #パケットロス率
            bandwidth, #帯域幅
            delay,#遅延
            network_event_scheduler #:NetworkGraph<?>
            )->None:

        self.network_event_scheduler = self.network_event_scheduler
        self.node_x = node_x
        self.node_y = node_y
        self.bandwidth = bandwidth
        self.delay = delay
        self.loss_rate = loss_rate
        self.packet_queue_xy = [] #パケットキュー(x→y)
        self.current_queue_time_xy = 0 #キューの時間(x→y)
        self.packet_queue_yx = [] #パケットキュー(y→x)
        self.current_queue_time_yx = 0 #キューの時間(y→x)
        #リンクを追加
        node_x.add_link(self)
        node_y.add_link(self)

        #グラフにリンクを追加
        label = f"{bandwidth/1000000}Mbps,{delay}s"
        self.network_event_scheduler.add_link(node_x.node_id,node_y.node_id,label,self.bandwidth,self.delay)

        #パケットをキューに追加するメゾット
        def enqueue_packet(self,packet,from_node):
            #流れる方向で分岐
            if from_node == self.node_x:
                queue = self.packet_queue_xy
                self.current_queue_time_xy = self.current_queue_time_xy
            else:
                queue = self.packet_queue_yx
                self.current_queue_time_yx = self.current_queue_time_yx

            #パケットの転送に必要な時間を計算
            packet_transfer_time = (packet.size * 8) / self.bandwidth
            #パケットのキュー予定時間を計算
            dequeue_time = self.network_event_scheduler.current_time + self.current_queue_time
            
            #パケットをキューに追加して、キュー時間を更新
            heapq.heappush(dequeue_time,packet,from_node)
            self.add_to_queue_time(from_node,packet_transfer_time)
            #一番だった場合の処理
            if len(queue == 1):
                self.network_event_scheduler.suchedule_event(dequeue_time,self.transfer_packet,from_node) 
 

        #パケットを転送するメゾット
        def transfer_packet(self,from_node):
            #流れる方向で分岐
            if from_node == self.node_x:
                queue = self.packet_queue_xy
            else:
                queue = self.packet_queue_yx

            if queue:
                dequeue_time,packet, _ = heapq.heappush(queue)
                packet_transfer_time = (packet.size * 8) /self.bandwidth
                
                #パケットロスを発生させる。
                if random.random() < self.loss_rate:
                    packet.set_arrived(-1) #フラグを付与

                next_node = self.node_x if from_node != self.node_x else node_y
                #遅延を考慮したイベントスケジュール
                self.network_event_scheduler.schedule_event(self.network_event_scheduler.current_time + self.delay,next_node.receive_packet,packet)
                self.network_event_scheduler.schedule_event(dequeue_time + packet_transfer_time,self.subtract_from_queue_time,from_node,packet_transfer_time)

                #次のパケットがある場合、そのイベントをスケジュールする。
                if queue:
                    next_packet_time = queue[0][0]
                    self.network_event_scheduler.sucedule_event(next_packet_time,self.transfer_packet,from_node)

    #キューの時間を増やす   
    def add_to_queue_time(self, from_node, packet_transfer_time):
        if from_node == self.node_x:
            self.current_queue_time_xy += packet_transfer_time
        else:
            self.cuurent_queue_time_yx += packet_transfer_time

    #キューの時間を減らす
    def subtract_from_queue_time(self, from_node, packet_transfer_time):
        if from_node == self.node_x:
            self.current_queue_time_xy -= packet_transfer_time
        else:
            self.current_queue_time_yx -= packet_transfer_time
    
    #次のノードへパケットを渡すメゾット
        #def transfer_packet(self,packet:Packet,from_node:Node)->None:
            #next_node = self.node_x if from_node != self.node_x else self.node_y
            #next_node.receive_packet(packet)

    #返却
    def __str__(self):
        return f"リンク({self.node_x.node_id} <-> {self.node_y.node_id}, 帯域幅:{self.bandwidth}, 遅延:{self.loss_rate}, パケットロス率:{self.packet_loss})"
        