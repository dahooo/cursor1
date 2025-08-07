import hashlib
import json
import time
from typing import Dict, Any


class Transaction:
    """
    交易類別 - 代表區塊鏈中的一筆交易
    """
    
    def __init__(self, from_address: str, to_address: str, amount: float, 
                 timestamp: float = None):
        """
        初始化交易
        
        Args:
            from_address: 發送方地址
            to_address: 接收方地址
            amount: 交易金額
            timestamp: 交易時間戳記
        """
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.timestamp = timestamp or time.time()
        self.transaction_id = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        計算交易的哈希值
        
        Returns:
            交易的 SHA-256 哈希值
        """
        transaction_string = json.dumps({
            "from_address": self.from_address,
            "to_address": self.to_address,
            "amount": self.amount,
            "timestamp": self.timestamp
        }, sort_keys=True)
        
        return hashlib.sha256(transaction_string.encode()).hexdigest()
    
    def is_valid(self) -> bool:
        """
        驗證交易是否有效
        
        Returns:
            交易是否有效
        """
        # 基本驗證規則
        if self.amount <= 0:
            return False
        
        if not self.from_address or not self.to_address:
            return False
        
        if self.from_address == self.to_address:
            return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        將交易轉換為字典格式
        
        Returns:
            交易的字典表示
        """
        return {
            "transaction_id": self.transaction_id,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "amount": self.amount,
            "timestamp": self.timestamp
        }
    
    def __str__(self) -> str:
        """
        交易的字符串表示
        """
        return f"Transaction: {self.from_address} -> {self.to_address} ({self.amount} coins)"