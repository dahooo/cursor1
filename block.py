import hashlib
import json
import time
from typing import List, Dict, Any, Optional


class Block:
    """
    區塊類別 - 代表區塊鏈中的一個區塊
    """
    
    def __init__(self, index: int, transactions: List[Dict[str, Any]], 
                 timestamp: float, previous_hash: str, nonce: int = 0):
        """
        初始化區塊
        
        Args:
            index: 區塊索引
            transactions: 交易列表
            timestamp: 時間戳記
            previous_hash: 前一個區塊的哈希值
            nonce: 工作量證明的隨機數
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        計算區塊的哈希值
        
        Returns:
            區塊的 SHA-256 哈希值
        """
        block_string = json.dumps({
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        """
        挖礦 - 工作量證明算法
        
        Args:
            difficulty: 挖礦難度（前導零的數量）
        """
        target = "0" * difficulty
        
        print(f"開始挖掘區塊 {self.index}...")
        start_time = time.time()
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        end_time = time.time()
        print(f"區塊 {self.index} 挖掘完成! 哈希值: {self.hash}")
        print(f"挖掘時間: {end_time - start_time:.2f} 秒")
        print(f"嘗試次數: {self.nonce}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        將區塊轉換為字典格式
        
        Returns:
            區塊的字典表示
        """
        return {
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }
    
    def __str__(self) -> str:
        """
        區塊的字符串表示
        """
        return f"Block #{self.index} [Hash: {self.hash[:16]}...]"