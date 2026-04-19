from __future__ import annotations 
import uuid

class Packet:
    def __init__(
            self,
            #発信元アドレス
            source:str,
            #宛先アドレス
            destination:str,
            #ペイロード,データ内容
            #payload:str,
            header_size:int,
            payload_size:int,
            network_event_scheduler:any
            )->None:
        

        self.network_event_scheduler = network_event_scheduler
        #パケットに一意のIDを付与。
        self.id = str(uuid.uuid4())

        self.header = {
             "source" : source,
             "destination" : destination,
        } 
        #パケットの実際の内容
        self.payload = 'A' * payload_size
        #パケットの実際の大きさ、容量
        self.size = header_size + payload_size
        #パケットに生成時刻
        self.creation_time = self.network_event_scheduler.current_time
        #パケットの到着時間
        self.arrival_time = None

    
    #到着時間をセット
    def set_arrived(self,arrival_time)->None:
         self.arrival_time = arrival_time

     #返却、文字列
    def __str__(self) -> str:
            return f"パケット(発信元:{self.header["source"]},宛先:{self.header["destination"]},ペイロード:{self.payload})"

    #後で設定する。優先順位を比較するため。一旦Falseにする。
    def __lt__(self, other):
         return False