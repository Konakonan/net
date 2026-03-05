from __future__ import annotations 


class Packet:
    def __init__(
            self,
            #発信元アドレス
            source:str,
            #宛先アドレス
            destination:str,
            #ペイロード,データ内容
            payload:str
            )->None:
        
        self.source = source
        self.destination = destination
        self.payload = payload

    def __str__(self) -> str:
            return f"パケット(発信元:{self.source},宛先:{self.destination},ペイロード:{self.payload})"