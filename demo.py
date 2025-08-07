#!/usr/bin/env python3
"""
私有區塊鏈示例程式
演示區塊鏈的基本功能
"""

from blockchain import Blockchain
from transaction import Transaction
import time

def print_separator(title=""):
    """打印分隔線"""
    print("\n" + "="*60)
    if title:
        print(f"  {title}")
        print("="*60)

def main():
    """主要示例程式"""
    print_separator("私有區塊鏈示例")
    
    # 1. 創建區塊鏈
    print("1. 創建新的區塊鏈...")
    blockchain = Blockchain(difficulty=2, mining_reward=100.0)
    print(f"區塊鏈創建完成: {blockchain}")
    
    print_separator("初始狀態")
    
    # 2. 顯示初始狀態
    print("2. 初始區塊鏈狀態:")
    print(f"   區塊數量: {len(blockchain.chain)}")
    print(f"   難度: {blockchain.difficulty}")
    print(f"   挖礦獎勵: {blockchain.mining_reward}")
    print(f"   區塊鏈有效性: {blockchain.is_chain_valid()}")
    
    print_separator("創建用戶和初始資金")
    
    # 3. 創建一些用戶地址
    alice = "Alice_0x1234"
    bob = "Bob_0x5678"
    charlie = "Charlie_0x9abc"
    
    print("3. 創建用戶:")
    print(f"   Alice: {alice}")
    print(f"   Bob: {bob}")
    print(f"   Charlie: {charlie}")
    
    # 4. 給 Alice 一些初始資金（通過挖礦）
    print("\n4. 給 Alice 提供初始資金...")
    
    # 創建一筆從系統到 Alice 的交易
    initial_transaction = Transaction("system", alice, 1000.0)
    blockchain.add_transaction(initial_transaction)
    
    # Alice 挖掘這個區塊獲得挖礦獎勵
    print("   Alice 開始挖礦...")
    blockchain.mine_pending_transactions(alice)
    
    print(f"   Alice 餘額: {blockchain.get_balance(alice)}")
    
    print_separator("交易測試")
    
    # 5. 創建一些交易
    print("5. 創建交易:")
    
    # Alice 向 Bob 轉帳 300
    tx1 = Transaction(alice, bob, 300.0)
    blockchain.add_transaction(tx1)
    print(f"   {tx1}")
    
    # Alice 向 Charlie 轉帳 200
    tx2 = Transaction(alice, charlie, 200.0)
    blockchain.add_transaction(tx2)
    print(f"   {tx2}")
    
    # 6. 挖掘交易
    print("\n6. Bob 挖掘待處理的交易...")
    blockchain.mine_pending_transactions(bob)
    
    print_separator("餘額檢查")
    
    # 7. 檢查所有用戶的餘額
    print("7. 用戶餘額:")
    print(f"   Alice: {blockchain.get_balance(alice)}")
    print(f"   Bob: {blockchain.get_balance(bob)}")
    print(f"   Charlie: {blockchain.get_balance(charlie)}")
    
    print_separator("更多交易")
    
    # 8. 更多交易
    print("8. 更多交易:")
    
    # Bob 向 Charlie 轉帳 150
    tx3 = Transaction(bob, charlie, 150.0)
    blockchain.add_transaction(tx3)
    print(f"   {tx3}")
    
    # Charlie 向 Alice 轉帳 100
    tx4 = Transaction(charlie, alice, 100.0)
    blockchain.add_transaction(tx4)
    print(f"   {tx4}")
    
    # Charlie 挖掘這些交易
    print("\n   Charlie 挖掘待處理的交易...")
    blockchain.mine_pending_transactions(charlie)
    
    print_separator("最終狀態")
    
    # 9. 最終餘額
    print("9. 最終餘額:")
    print(f"   Alice: {blockchain.get_balance(alice)}")
    print(f"   Bob: {blockchain.get_balance(bob)}")
    print(f"   Charlie: {blockchain.get_balance(charlie)}")
    
    # 10. 區塊鏈統計
    print("\n10. 區塊鏈統計:")
    print(f"    總區塊數: {len(blockchain.chain)}")
    print(f"    總交易數: {sum(len(block.transactions) for block in blockchain.chain)}")
    print(f"    區塊鏈有效性: {blockchain.is_chain_valid()}")
    
    print_separator("區塊詳情")
    
    # 11. 顯示所有區塊
    print("11. 區塊鏈詳情:")
    for i, block in enumerate(blockchain.chain):
        print(f"\n    區塊 {i}:")
        print(f"      哈希: {block.hash}")
        print(f"      前一個哈希: {block.previous_hash}")
        print(f"      時間戳: {time.ctime(block.timestamp)}")
        print(f"      交易數量: {len(block.transactions)}")
        print(f"      Nonce: {block.nonce}")
        
        if block.transactions:
            print("      交易:")
            for j, tx in enumerate(block.transactions):
                print(f"        {j+1}. {tx.get('from_address', 'N/A')} -> "
                      f"{tx.get('to_address', 'N/A')}: {tx.get('amount', 0)} coins")
    
    print_separator("交易歷史")
    
    # 12. 顯示用戶交易歷史
    print("12. 用戶交易歷史:")
    for user, address in [("Alice", alice), ("Bob", bob), ("Charlie", charlie)]:
        print(f"\n    {user} 的交易歷史:")
        history = blockchain.get_transaction_history(address)
        for tx_record in history:
            tx = tx_record['transaction']
            block_idx = tx_record['block_index']
            if tx.get('from_address') == address:
                print(f"      區塊 {block_idx}: 發送 {tx.get('amount')} 給 {tx.get('to_address')}")
            else:
                print(f"      區塊 {block_idx}: 接收 {tx.get('amount')} 來自 {tx.get('from_address')}")
    
    print_separator("測試無效交易")
    
    # 13. 測試無效交易
    print("13. 測試無效交易:")
    
    # Alice 嘗試發送超過餘額的金額
    invalid_tx = Transaction(alice, bob, 10000.0)
    success = blockchain.add_transaction(invalid_tx)
    print(f"    Alice 嘗試發送 10000 (餘額不足): {'成功' if success else '失敗'}")
    
    # 嘗試發送負數金額
    negative_tx = Transaction(alice, bob, -100.0)
    success = blockchain.add_transaction(negative_tx)
    print(f"    嘗試發送負數金額: {'成功' if success else '失敗'}")
    
    print_separator("保存區塊鏈")
    
    # 14. 保存區塊鏈到文件
    print("14. 保存區塊鏈到文件...")
    blockchain.save_to_file("demo_blockchain.json")
    
    print_separator("示例完成")
    print("區塊鏈示例程式執行完成!")
    print("你可以:")
    print("1. 查看 demo_blockchain.json 文件以檢查保存的區塊鏈")
    print("2. 運行 'python api.py' 啟動 API 服務器")
    print("3. 使用 API 與區塊鏈互動")

def test_blockchain_validation():
    """測試區塊鏈驗證功能"""
    print_separator("區塊鏈驗證測試")
    
    print("創建測試區塊鏈...")
    blockchain = Blockchain(difficulty=1)
    
    # 添加一些交易並挖掘
    tx = Transaction("test_user1", "test_user2", 50.0)
    blockchain.add_transaction(tx)
    blockchain.mine_pending_transactions("miner1")
    
    print(f"區塊鏈有效性: {blockchain.is_chain_valid()}")
    
    # 嘗試篡改區塊鏈
    print("\n嘗試篡改第二個區塊的交易...")
    if len(blockchain.chain) > 1:
        blockchain.chain[1].transactions[0]['amount'] = 1000000  # 篡改金額
        print(f"篡改後區塊鏈有效性: {blockchain.is_chain_valid()}")
    
    print("區塊鏈驗證測試完成!")

if __name__ == "__main__":
    main()
    print("\n" + "="*60)
    test_blockchain_validation()