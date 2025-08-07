#!/usr/bin/env python3
"""
測試 API 的簡單腳本
"""

import requests
import json
import time

def test_api():
    """測試 API 端點"""
    base_url = "http://localhost:5000"
    
    print("=== 區塊鏈 API 測試 ===")
    
    try:
        # 1. 測試根端點
        print("1. 測試 API 資訊...")
        response = requests.get(f"{base_url}/")
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        # 2. 測試區塊鏈狀態
        print("\n2. 測試區塊鏈狀態...")
        response = requests.get(f"{base_url}/blockchain")
        print(f"狀態碼: {response.status_code}")
        blockchain_data = response.json()
        print(f"區塊數量: {blockchain_data['length']}")
        print(f"有效性: {blockchain_data['valid']}")
        
        # 3. 測試創建交易
        print("\n3. 測試創建交易...")
        transaction_data = {
            "from_address": "Alice_0x1234",
            "to_address": "Bob_0x5678", 
            "amount": 50.0
        }
        response = requests.post(f"{base_url}/transaction", 
                               json=transaction_data,
                               headers={'Content-Type': 'application/json'})
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        # 4. 測試挖礦
        print("\n4. 測試挖礦...")
        mining_data = {
            "mining_reward_address": "Miner_0x9abc"
        }
        response = requests.post(f"{base_url}/mine",
                               json=mining_data,
                               headers={'Content-Type': 'application/json'})
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        # 5. 測試餘額查詢
        print("\n5. 測試餘額查詢...")
        response = requests.get(f"{base_url}/balance/Miner_0x9abc")
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        # 6. 測試統計資訊
        print("\n6. 測試統計資訊...")
        response = requests.get(f"{base_url}/stats")
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        print("\n=== API 測試完成 ===")
        
    except requests.exceptions.ConnectionError:
        print("錯誤: 無法連接到 API 服務器")
        print("請確保 API 服務器正在運行 (python3 api.py)")
    except Exception as e:
        print(f"測試過程中發生錯誤: {e}")

if __name__ == "__main__":
    test_api()