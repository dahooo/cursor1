import time
import json
from typing import List, Dict, Any, Optional
from block import Block
from transaction import Transaction


class Blockchain:
    """
    區塊鏈類別 - 管理整個區塊鏈
    """
    
    def __init__(self, difficulty: int = 2, mining_reward: float = 100.0):
        """
        初始化區塊鏈
        
        Args:
            difficulty: 挖礦難度
            mining_reward: 挖礦獎勵
        """
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.mining_reward = mining_reward
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """
        創建創世區塊
        """
        genesis_block = Block(
            index=0,
            transactions=[],
            timestamp=time.time(),
            previous_hash="0"
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        print("創世區塊已創建!")
    
    def get_latest_block(self) -> Block:
        """
        獲取最新的區塊
        
        Returns:
            最新的區塊
        """
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """
        添加交易到待處理列表
        
        Args:
            transaction: 要添加的交易
            
        Returns:
            是否成功添加交易
        """
        if not transaction.is_valid():
            print(f"無效交易: {transaction}")
            return False
        
        # 檢查發送方是否有足夠的餘額（除了挖礦獎勵交易）
        if transaction.from_address != "system":
            balance = self.get_balance(transaction.from_address)
            if balance < transaction.amount:
                print(f"餘額不足: {transaction.from_address} 餘額 {balance}, 嘗試發送 {transaction.amount}")
                return False
        
        self.pending_transactions.append(transaction)
        print(f"交易已添加到待處理列表: {transaction}")
        return True
    
    def mine_pending_transactions(self, mining_reward_address: str) -> bool:
        """
        挖掘待處理的交易
        
        Args:
            mining_reward_address: 接收挖礦獎勵的地址
            
        Returns:
            是否成功挖掘
        """
        if not self.pending_transactions:
            print("沒有待處理的交易")
            return False
        
        # 添加挖礦獎勵交易
        reward_transaction = Transaction(
            from_address="system",
            to_address=mining_reward_address,
            amount=self.mining_reward
        )
        self.pending_transactions.append(reward_transaction)
        
        # 創建新區塊
        new_block = Block(
            index=len(self.chain),
            transactions=[tx.to_dict() for tx in self.pending_transactions],
            timestamp=time.time(),
            previous_hash=self.get_latest_block().hash
        )
        
        # 挖掘區塊
        new_block.mine_block(self.difficulty)
        
        # 添加到區塊鏈
        self.chain.append(new_block)
        
        # 清空待處理交易
        self.pending_transactions = []
        
        print(f"區塊 {new_block.index} 已成功添加到區塊鏈!")
        return True
    
    def get_balance(self, address: str) -> float:
        """
        獲取地址的餘額
        
        Args:
            address: 要查詢的地址
            
        Returns:
            地址的餘額
        """
        balance = 0.0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.get("from_address") == address:
                    balance -= transaction.get("amount", 0)
                
                if transaction.get("to_address") == address:
                    balance += transaction.get("amount", 0)
        
        return balance
    
    def is_chain_valid(self) -> bool:
        """
        驗證區塊鏈是否有效
        
        Returns:
            區塊鏈是否有效
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # 檢查當前區塊的哈希是否正確
            if current_block.hash != current_block.calculate_hash():
                print(f"區塊 {i} 的哈希值無效")
                return False
            
            # 檢查區塊是否正確連接到前一個區塊
            if current_block.previous_hash != previous_block.hash:
                print(f"區塊 {i} 的前一個哈希值無效")
                return False
            
            # 檢查工作量證明
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                print(f"區塊 {i} 的工作量證明無效")
                return False
        
        return True
    
    def get_transaction_history(self, address: str) -> List[Dict[str, Any]]:
        """
        獲取地址的交易歷史
        
        Args:
            address: 要查詢的地址
            
        Returns:
            交易歷史列表
        """
        transactions = []
        
        for block in self.chain:
            for transaction in block.transactions:
                if (transaction.get("from_address") == address or 
                    transaction.get("to_address") == address):
                    transactions.append({
                        "block_index": block.index,
                        "transaction": transaction,
                        "timestamp": transaction.get("timestamp")
                    })
        
        return transactions
    
    def to_dict(self) -> Dict[str, Any]:
        """
        將區塊鏈轉換為字典格式
        
        Returns:
            區塊鏈的字典表示
        """
        return {
            "chain": [block.to_dict() for block in self.chain],
            "difficulty": self.difficulty,
            "pending_transactions": [tx.to_dict() for tx in self.pending_transactions],
            "mining_reward": self.mining_reward
        }
    
    def save_to_file(self, filename: str) -> None:
        """
        將區塊鏈保存到文件
        
        Args:
            filename: 文件名
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        print(f"區塊鏈已保存到 {filename}")
    
    def __str__(self) -> str:
        """
        區塊鏈的字符串表示
        """
        return f"Blockchain with {len(self.chain)} blocks, difficulty: {self.difficulty}"